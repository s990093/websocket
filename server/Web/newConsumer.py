from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import datetime
from rich import pretty
from rich.console import Console

pretty.install()
console = Console()

class MouseConsumer(WebsocketConsumer):
    def connect(self):
        """
        Method called when a WebSocket connection is established.
        Initializes the chat room and adds the current channel to the group.
        """
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        """
        Method called when the WebSocket connection is closed.
        Removes the current channel from the group.
        """
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)

        async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': text_data_json
                    }
                )
    

    def chat_message(self, event):
        message = event['message']
        
        print(message)

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))