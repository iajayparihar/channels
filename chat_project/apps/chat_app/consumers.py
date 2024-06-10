import json
from channels.consumer import SyncConsumer, AsyncConsumer

class ChatConsumer(SyncConsumer):
    def websocket_connect(self,event):
        print('websocket connected event', event)
        self.send({
            'type': 'websocket.accept'
        })
    def websocket_disconnect(self, event):
        print('websocket is disconnected', event)

    def websocket_receive(self, event):
        print('message recevied ...', event )
        print('message is ',event['text'])
