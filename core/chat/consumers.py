from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from api_interface.models import StudentSubjectAttendance
from threading import Thread
from core.room.models import Room


def present_add(username, room_id):
    try:
        room = Room.objects.get(public_id=room_id)
        attendance = StudentSubjectAttendance.objects.get(student_fk__username=username,
                                                          subject_fk__subject_code=int(room.name))
        attendance.attendance += 1
        attendance.save()
        print("Attendance Updated Successful")
    except:
        print("Ether a teacher or admin or someone unknown has joined.")


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self, **kwargs):
        self.room_name = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = self.room_name
        t = Thread(target=present_add, kwargs={
            "username": self.scope['url_route']['kwargs']['username'],
            "room_id": self.room_name
        })
        t.start()
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        t.join()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        receive_dict = json.loads(text_data)
        message = receive_dict["message"]

        action = receive_dict['action']

        if action in ['new-offer', 'new-answer']:
            receiver_channel_name = receive_dict['message']['receiver_channel_name']

            receive_dict['message']['receiver_channel_name'] = self.channel_name

            await self.channel_layer.send(
                receiver_channel_name,
                {
                    'type': 'send.sdp',
                    'receive_dict': receive_dict
                }
            )
            return

        receive_dict['message']['receiver_channel_name'] = self.channel_name

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send.sdp',
                'receive_dict': receive_dict
            }
        )

    async def send_sdp(self, event):
        receive_dict = event["receive_dict"]

        await self.send(
            text_data=json.dumps(receive_dict)
        )
