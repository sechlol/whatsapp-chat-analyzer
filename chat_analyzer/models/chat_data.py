from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Message:
    sender: str
    date: datetime
    text: str


@dataclass
class Chat:
    participants: List[str] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)

    def add_message(self, message: Message):
        self.messages.append(message)
        if message.sender not in self.participants:
            self.participants.append(message.sender)
