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
        """
        Method called when a message is received from the WebSocket.
        Processes the message and sends it to the group if it is valid.
        """
        try:
            text_data_json = json.loads(text_data)
            device = text_data_json.get('device')

            console.print(f"device: {text_data_json}")

            if device == 'mobile':
                action = text_data_json.get('action')
                if action == 'double':
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'broadcast_message',
                            'message': 'Right click detected!',
                            'coordinates': text_data_json.get('coordinates', {})
                        }
                    )
                elif action == 'mouse_move':
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'broadcast_message',
                            'message': 'Mouse moved!',
                            'coordinates': text_data_json.get('coordinates', {})
                        }
                    )
          
        except json.JSONDecodeError:
            console.print("Received message is not in JSON format", style="bold red")

    def broadcast_message(self, event):
        """
        Method called when a broadcast message is received from the group.
        Sends the message to the WebSocket.
        """
        message = event['message']
        response = {
            'message': message,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        if 'coordinates' in event:
            response['coordinates'] = event['coordinates']
        if 'speed' in event:
            response['speed'] = event['speed']
        self.send(text_data=json.dumps(response))
