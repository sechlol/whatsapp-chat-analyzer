from datetime import datetime
from typing import List


class Message:
    sender: str
    date: datetime
    text: str

    def __init__(self, sender: str, date: datetime, text: str):
        self.sender = sender
        self.date = date
        self.text = text


class Chat:
    participants: List[str] = []
    messages: List[Message] = []

    def add_message(self, message: Message):
        self.messages.append(message)
        if message.sender not in self.participants:
            self.participants.append(message.sender)
