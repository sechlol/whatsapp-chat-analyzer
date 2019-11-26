from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict

from chat_analyzer.models.chat_schemas import ChatMessageStatSchema, StatsWrapperSchema


@dataclass
class Message:
    sender: str
    date: datetime
    text: str


@dataclass
class Chat:
    name: str
    participants: List[str] = field(default_factory=list)
    messages: List[Message] = field(default_factory=list)

    def add_message(self, message: Message):
        self.messages.append(message)
        if message.sender not in self.participants:
            self.participants.append(message.sender)


@dataclass
class UserMessageStat:
    username: str
    message_count: int
    message_percent: float
    word_count: int
    word_percent: float
    avg_words_per_message: float


@dataclass
class ChatMessageStat:
    total_messages_count: int
    total_words_count: int
    user_stats: List[UserMessageStat]

    def to_json(self):
        return ChatMessageStatSchema().dump(self)


@dataclass
class Score:
    label: str
    value: float


@dataclass
class MessagesPerDayStat:
    date_sent: date
    scores: List[Score]

    def get_labels(self) -> List[str]:
        return [s.label for s in self.scores]

    def get_indexed_values(self) -> Dict[str, float]:
        return {s.label: s.value for s in self.scores}


@dataclass
class StatsWrapper:
    legend: List[str]
    stats: List[MessagesPerDayStat]

    def get_sorted_dates(self) -> List[date]:
        return [s.date_sent for s in self.stats]

    def get_indexed_by_date(self) -> Dict[date, MessagesPerDayStat]:
        return {s.date_sent: s for s in self.stats}

    def get_indexed_by_date_raw(self) -> Dict[date, Dict[str, float]]:
        return {s.date_sent: s.get_indexed_values() for s in self.stats}

    def to_json(self):
        return StatsWrapperSchema().dump(self)
