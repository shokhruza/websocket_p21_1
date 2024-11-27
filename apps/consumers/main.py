from django.forms import model_to_dict

from apps.consumers.base import CustomAsyncJsonWebsocketConsumer
from apps.models import Message


class ChatConsumer(CustomAsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.room_group_name = None
        self.room = None
        self.user = None
        self.user_inbox = None

    async def connect(self):
        self.user = self.scope['user']
        # connection has to be accepted
        await self.accept()
        if not await self.is_authenticate():
            return
        # self.room_name = self.scope['url_route']['kwargs']['room_name']
        # self.room_group_name = f'chat_{self.room_name}'
        # self.room = await Chat.objects.aget(name=self.room_name)
        self.user_inbox = f'inbox_{self.user.id}'

        # # join the room group
        # await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # send the user list to the newly joined user
        # user_list = []
        # async for user in self.room.online.all():
        #     user_list.append(user.username)
        #
        # await self.send_json({
        #     'type': 'user_list',
        #     'users': user_list,
        # })

        # create a user inbox for private messages
        await self.channel_layer.group_add(self.user_inbox, self.channel_name)

        # send the join event to the room
        await self.notify_status()
        await self.update_user_status()
        # await self.room_update_user(self.room, self.user)

    async def notify_status(self, is_connected: bool = True):
        pass
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'user_join',
        #         'user': model_to_dict(self.user, ('id', 'username')),
        #     }
        # )

    # @sync_to_async
    # def room_update_user(self, room, user, action: str = 'add'):
    #     getattr(room.online, action)(user)

    async def disconnect(self, close_code):
        # delete the user inbox for private messages
        await self.update_user_status(False)
        await self.channel_layer.group_discard(self.user_inbox, self.channel_name)

        # # send the leave event to the room
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'user_leave',
        #         'user': self.user.username,
        #     }
        # )
        # self.room_update_user(self.room, self.user, 'remove')

    async def receive_json(self, content, **kwargs):
        if not (len(set(content) & {'target', 'type' , 'message'}) > 2):
            await self.send_json({'message': 'xabar yuboriladigan chat idni kiriting'})
            return

        if content['type'] == 'private':
            msg = await Message.objects.acreate(from_user=self.user, to_user_id=content['target'], text=content['message'])

            # send private message to the target
            await self.channel_layer.group_send(
                f"inbox_{content['target']}",
                {
                    'type': 'chat_message',
                    'user': model_to_dict(self.user, ('id', 'username')),
                    'message': model_to_dict(msg, ('id', 'text')),
                }
            )
        return
        #
        # # send chat message event to the room
        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'user': model_to_dict(self.user, ('id', 'username')),
        #         'message': content['message'],
        #     }
        # )

    async def chat_message(self, event):
        await self.send_json(event)

    async def user_join(self, event):
        await self.send_json(event)

    async def user_leave(self, event):
        await self.send_json(event)

    # async def private_message(self, event):
    #     await self.send_json(event)
    #
    # async def private_message_delivered(self, event):
    #     await self.send_json(event)


'''

901001011
ws://localhost:8000/ws/chat?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NjQ0NzI0LCJpYXQiOjE3MjczNDg3MjQsImp0aSI6IjUwZGY1ODdiMjEyNjQ3NGRhNjA1ZGU2YmZkOThkNGE0IiwidXNlcl9pZCI6Mn0.1s7A3icj0DZrjB_qKKkEKeFFFLNyjVpFjR1UmuN2Vx8


901001012
ws://localhost:8000/ws/chat?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NjQ0NzU4LCJpYXQiOjE3MjczNDg3NTgsImp0aSI6IjZlYjBlMTQzNjA1ODRkODM4OGJkNGFmYmY3OGNhOTMxIiwidXNlcl9pZCI6M30.S0YEPOLR5whhPw7cKyNTw300XHOIj51NK7u4wKY3cPI


901001013
ws://localhost:8000/ws/chat?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI4NjQ0Nzc3LCJpYXQiOjE3MjczNDg3NzcsImp0aSI6IjgxNTQ3Mjc1NWZjODQyNDA5NWM0YTM5OTM5ZmZlOTA2IiwidXNlcl9pZCI6NH0.INIl9g1NjHvZ-gnrrpqZkzTFNBcokxDewLQ0Tw4XIos


'''