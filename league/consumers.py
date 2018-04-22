from channels.generic.websocket import WebsocketConsumer
from channels.consumer import SyncConsumer
from channels.layers import get_channel_layer

import json

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        print(self.scope["user"])
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json       
        channel_layer = get_channel_layer()        
