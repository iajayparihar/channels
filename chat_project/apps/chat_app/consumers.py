import json
from channels.consumer import SyncConsumer, AsyncConsumer, StopConsumer
from asgiref.sync import async_to_sync, sync_to_async
from chat_app.models import ChatModel,GroupModel

class ChatSyncConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('websocket connected event', event)
        print('channel layes ', self.channel_layer)
        print('channel name ', self.channel_name)
        print(self.scope['url_route']['kwargs']["groupName"], "is Group Name !!!")
        self.Group_name = self.scope['url_route']['kwargs']["groupName"]
#           self.channel_layer.group_add        group_add is async method so convert it to sync with async_to_sync
        async_to_sync(self.channel_layer.group_add)(self.Group_name, self.channel_name)

        self.send({
            'type': 'websocket.accept'
        })

    def websocket_disconnect(self, event):
        print('websocket is disconnected', event)
        print('channel layes ', self.channel_layer)
        print('channel name ', self.channel_name)
        async_to_sync(self.channel_layer.group_discard)(self.Group_name, self.channel_name)
        raise StopConsumer()
    
    def websocket_receive(self, event):
        print('message recevied ...', event )
        print('message is ',event['text'])
        
        # sending to group 
        async_to_sync(self.channel_layer.group_send)(self.Group_name,{
            'type' : 'chat.message', # chat.message is calling chat_message function
            'message' : event['text'],
        })
        
        # sending to client for displaying message 
    def chat_message(self,event):        
        self.send({
            'type': 'websocket.send',
            'text': event['message'],
        })


class ChatASyncConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('websocket connected event', event)
        print('channel layes ', self.channel_layer)
        print('channel name ', self.channel_name)
        self.Group_name = self.scope['url_route']['kwargs']["groupName"]
        print('Group name is : ', self.Group_name)
        
        await self.channel_layer.group_add(self.Group_name, self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_disconnect(self, event):
        print('websocket is disconnected', event)
        print('channel layes ', self.channel_layer)
        print('channel name ', self.channel_name)
        await self.channel_layer.group_discard(self.Group_name, self.channel_name)
        raise StopConsumer()
    
    async def websocket_receive(self, event):
        print('message recevied ...', event )
        print('message is ',event['text'])
        # import pdb;pdb.set_trace();
        data = json.loads(event['text'])

        group = await sync_to_async(GroupModel.objects.get)(name=self.Group_name)

        # Save the message to the database
        await sync_to_async(ChatModel.objects.create)(content=data['message'], group=group)

        # sending to group 
        await self.channel_layer.group_send(self.Group_name,{
            'type' : 'chat.message', # chat.message is calling chat_message function
            'message' : event['text'],
        })
        
        # sending to client for displaying message 
    async def chat_message(self,event):        
        await self.send({
            'type': 'websocket.send',
            'text': event['message'],
        })

