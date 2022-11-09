from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json


class AccessOne(WebsocketConsumer):
    def connect(self):
        self.room_name = "AccessOne"
        self.room_group_name = "AccessOne_Group"
        print("Connecting*********")
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
            )
        self.accept()
        
        
    def disconnect(self):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, 
            self.channel_name
        )
        
    def receive(self, text_data):
        print(text_data)
        self.send(text_data=json.dumps({"status": "received"}))
        
    def status(self, event):
        data = json.loads(event['value'])
        print(data)
        self.send(text_data=json.dumps({
            "data": data
            }))