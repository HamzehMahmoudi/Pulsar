import json
from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from chat.models import Chat, Message
from accounts.models import ProjectUser
from urllib.parse import parse_qs
# from chat.models import Message
# from account.models import User

@sync_to_async
def consumer_authenticator(user=None, project_uuid=None, project_user=None, chat_id=None):
    if user.is_authenticated:
        project = user.projects.filter(pk=project_uuid).last()
        if project is None:
            res = False
        else:
            chat = project.chats.filter(pk=chat_id).last()
            if chat is None:
                res = False
            else:    
                res = chat.members.filter(pk=project_user).exists()
    else:
        res = False
    return res
    

class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['id']
        self.user = self.scope['user']
        self.qs = parse_qs(self.scope['query_string'].decode())
        self.project = self.qs.get('project', [None])[0]
        self.project_user = self.qs.get('project_user', [None])[0]
        self.group_name = f"chat{self.chat_id}"
        auth = await consumer_authenticator(chat_id=self.chat_id, user=self.user, project_uuid=self.project, project_user=self.project_user)
        if auth:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            # async_to_sync(self.channel_layer.group_add)(
            #     self.group_name,
            #     self.channel_name
            # )
            self.project_user  = await ProjectUser.objects.aget(pk=self.project_user)
            print("connected")
            await self.accept()
            self.project_user.is_online = True
            async_to_sync(self.user.save)
        else:
            await self.disconnect()
            
        # if self.chat is not None and self.user.is_authenticated:
        #     # Join room group
        #     await self.channel_layer.group_add(self.group_name, self.channel_name)
        #     # async_to_sync(self.channel_layer.group_add)(
        #     #     self.group_name,
        #     #     self.channel_name
        #     # )
        #     print("connected")
        #     await self.accept()
        #     self.user.is_online = True
        #     async_to_sync(self.user.save)
        # else:
        #     await self.disconnect()

    async def disconnect(self, close_code=1):
        # Leave room group
        print('disconnected')
        if self.project_user.is_online:  
            self.user.is_online = False
            async_to_sync(self.user.save)

        # async_to_sync(self.channel_layer.group_discard)(
        #     self.group_name,
        #     self.channel_name
        # )
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
    # Receive message from WebSocket

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            send_method = self.commands.get(data.get('command'))
            await send_method(self, data)
        except Exception as e:
            await self.send_message({'error': str(e)})

    async def fetch_messages(self, data):
        content = {
            'command': 'messages',
            'messages': self.chat.messages_to_json()
        }
        # BroadCast that message
        await self.send_message(content)

    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))

    async def new_message(self, data):
        # gets the new message creates a model from it and sends it to bradcast
        message = await Message.objects.acreate(
            user=self.user,
            text=data['message'],
            chat=self.chat)
        content = {
            'command': 'new_message',
            'message': message.message_tojson()
        }
        return await self.send_chat_message(content)

    async def send_chat_message(self, message):
        data = {
            'type': 'chat_message',
            'message': message
        }
        # Send message to room group
        # async_to_sync(self.channel_layer.group_send)(
        #     self.group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': message
        #     }
        # )
        await self.channel_layer.group_send(self.group_name, data)
    # Receive message from room group

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))

    async def is_typing(self, event):
        content = {
            'command': 'is_typing',
            'user_id': self.user.id,
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

    # Helper Function for turning message to JSON

    # def message_to_json(self, message):
    #     return {
    #         'id': message.id,
    #         'author': message.contact.user.username,
    #         'content': message.content,
    #         'timestamp': str(message.timestamp)
    #     }

    # Helper Function for turning multiple messages to JSON List
    # def messages_to_json(self, messages):
    #     result = []
    #     for message in messages:
    #         result.append(self.message_to_json(message))
    #     return result
