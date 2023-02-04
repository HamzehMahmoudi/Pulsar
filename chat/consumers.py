import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from chat.models import Chat, Message
from chat.utils import get_from_base64
# from chat.models import Message
# from account.models import User


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
                async_to_sync(self.project_user.save)
                self.chat = await Chat.objects.aget(pk=self.chat_id)
                await self.accept()
                await self.send_message({'key': self.chat.key})
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
                async_to_sync(self.project_user.save)
        # if error_msg is not None:
            # await self.send_json({'error': error_msg}, close=True)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    # Receive message from WebSocket

    async def receive(self, text_data, **kwargs):
        try:
            data = json.loads(text_data)
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
        # BroadCast that message
        await self.send_message(content)

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def new_message(self, data):
        # gets the new message creates a model from it and sends it to bradcast
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
            replied_on=data.get('replied_on'))
        host = await self.get_host()
        content = {
            'command': 'new_message',
            'message': message.message_tojson(host=host)
        }
        return await self.send_chat_message(content)

    async def send_chat_message(self, message):
        data = {
            'type': 'chat_message',
            'message': message
        }
        await self.channel_layer.group_send(self.group_name, data)
    # Receive message from room group

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def is_typing(self, event):
        content = {
            'command': 'is_typing',
            'user_id': self.project_user.id,
            'message': event["is_typing"]
        }
        print(content['message'], type(content['message']))
        await self.send_chat_message(content)
    # Identify the socket request and open respected proccess
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message,
        'is_typing': is_typing,
    }
