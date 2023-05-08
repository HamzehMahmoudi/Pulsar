import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chat.models import Chat, Message
from chat.utils import get_from_base64, encrypt_message, decrypt_message
from django.conf import settings


enc = settings.ENCRYPTION

async def costumer_authenticator(project=None, project_user=None, chat_id=None):
    if not project or not project_user or not chat_id:
        return False
    project_user_condition = project_user.project_id == project.id
    chat_condition = await project.chats.filter(pk=chat_id, members=project_user).aexists()
    return project_user_condition and chat_condition



class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def get_host(self):
        scope = self.scope
        from accounts.auth import get_headers
        headers = get_headers(scope=scope)
        con_type = scope.get("type", None)
        if con_type == "websocket":
            protocol = "http"
        elif con_type == "websocket secure":
            protocol = "https"
        else:
            protocol = None
        host = headers.get('host', None)
        if host is not None and protocol is not None:
            return f"{protocol}://{host}" 
        return None

    async def connect(self):
        try:
            self.chat_id = self.scope['url_route']['kwargs']['id']
            self.project = self.scope['project']
            self.project_user = self.scope['project_user']
            self.group_name = f"chat{self.chat_id}"
            self.is_authenticated =  await costumer_authenticator(project=self.project, project_user=self.project_user, chat_id=self.chat_id)
            if self.is_authenticated:
                await self.channel_layer.group_add(self.group_name, self.channel_name)
                print("connected")
                self.project_user.is_online = True
                self.chat = await Chat.objects.aget(pk=self.chat_id)
                self.key = self.chat.key
                sync_to_async(self.project_user.save)()
                await self.accept()
                # await self.send_message({'key': self.chat.key},enc=False) # add system to exchange keies
            else:
                await self.disconnect(error_msg='authentication required')
        except Exception as e:
            await self.disconnect(error_msg=str(e))

    async def disconnect(self, error_msg=None):
        # Leave room group
        print('disconnected')
        if self.project_user is not None:
            if self.project_user.is_online:  
                self.project_user.is_online = False
                sync_to_async(self.project_user.save)()
        # if error_msg is not None:
            # await self.send_json({'error': error_msg}, close=True)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)


    async def receive(self, text_data, enc=enc, **kwargs):
            try:
                if enc:
                    decrypted_message = await sync_to_async(decrypt_message)(text_data, key=self.key)
                else:
                    decrypted_message = text_data
                data = json.loads(decrypted_message)
                send_method = self.commands.get(data.get('command'))
                await send_method(self, data)
            except Exception as e:
                await self.send_message({'error': str(e)})
                
    async def fetch_messages(self, data):
        host = await self.get_host()
        content = {
            'command': 'messages',
            'messages': await sync_to_async(self.chat.messages_to_json)(host=host)
        }

        await self.send_message(content)

    async def send_message(self, message, enc=enc):
        """
        encrypt data 
        """
        json_data = json.dumps(message)
        try:
            if enc:
                encrypted_data = await sync_to_async(encrypt_message)(message=json_data, key=self.chat.key)
            else:
                encrypted_data = json_data
            await self.send(text_data=encrypted_data)
        except Exception as e:
            print(e)
            
    async def send_chat_message(self, message):
        data = {
            'type': 'chat_message',
            'message': message
        }
        await self.channel_layer.group_send(self.group_name, data)

    async def chat_message(self, event):
        message = event['message']
        await self.send_message(message)
        
    async def new_message(self, data):

        file_data=data.get('message_file')
        file_name=data.get('filename')
        message_file =None
        if file_data is not None and file_name is not None:
            message_file = get_from_base64(file_data=file_data, filename=file_name)
        message = await Message.objects.acreate(
            user=self.project_user,
            text=data.get('message'),
            message_file = message_file,
            chat_id=self.chat_id,
            replied_on_id=data.get('replied_on'))
        host = await self.get_host()
        content = {
            'command': 'new_message',
            'message': await sync_to_async(message.message_tojson)(host=host)
        }
        await self.send_chat_message(content)


    async def is_typing(self, data):
        content = {
            'command': 'is_typing',
            'user_id': self.project_user.id,
            'message': data["is_typing"]
        }
        print(content['message'], type(content['message']))
        await self.send_chat_message(content)
        
    async def edit_message(self, data):

        message_id=data.get('message_id')
        message = await Message.objects.filter(chat=self.chat, pk=message_id, user=self.project_user).alast()
        if message is not None:            
            message.text=data.get('message')
            await sync_to_async(message.save)()
            host = await self.get_host()
            content = {
                'command': 'edit_message',
                'edited_id': message_id ,
                'message': await sync_to_async(message.message_tojson)(host=host),
                'status': 200,
            }
        else:
            content = {
                'command': 'edit_message',
                'edited_id': message_id ,
                'message': None,
                'status': 400,
            }           
        await self.send_chat_message(content)
    
    async def delete_message(self, data):
        # gets the new message delete a model from it and sends it to bradcast
        #data = json.loads(data.get("msg", {}))
        message_id=data.get('message_id')
        message = await Message.objects.filter(chat=self.chat, pk=message_id, user=self.project_user).alast()
        if message is not None:
            await sync_to_async(message.delete)()        
            content = {
                'command': 'delete_message',
                'deleted_id': message_id ,
                'status': 200,
            }
        else:
            content = {
                'command': 'delete_message',
                'deleted_id': message_id ,
                'status': 400,
            }           
        await self.send_chat_message(content)
    
    async def forward_message(self, data):
        ...
    
    async def read_messages(self, data):
        messages_ids = data.get('message_ids', [])
        messages = self.chat.messages.filter(pk__in=messages_ids)
        ids = []
        async for message in messages:
           await sync_to_async(message.views.add)(self.project_user)
           ids.append(message.pk)
    
        content = {
                'command': 'read_messages',
                'readed_ids':  ids,
                'status': 200,
            } 
        await self.send_chat_message(content)
        
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'edit_message': edit_message,
        'delete_message': delete_message,
        'is_typing': is_typing,
        'forward_message': forward_message,
        'read_messages': read_messages
    }
