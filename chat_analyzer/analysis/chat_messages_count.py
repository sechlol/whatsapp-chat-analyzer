from dataclasses import dataclass
from typing import List

from analysis.utils import _get_words_from_text
from chat_data import Chat


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


def messages_per_user_count(chat: Chat) -> ChatMessageStat:
    participants = {}
    total_words = 0
    for message in chat.messages:
        words_count = len(_get_words_from_text(message.text))
        prev_count = participants.get(message.sender, (0, 0))

        # [0] = total message count
        # [1] = total word count
        participants[message.sender] = (prev_count[0] + 1, prev_count[1] + words_count)
        total_words += words_count

    user_stats = []
    for sender, count in participants.items():
        percent_message = count[0] / len(chat.messages)
        percent_words = count[1] / total_words
        user_stats.append(UserMessageStat(
            username=sender,
            message_count=count[0],
            message_percent=round(percent_message, 4),
            word_count=count[1],
            word_percent=round(percent_words, 4),
            avg_words_per_message=round(count[1] / count[0], 2))
        )

    return ChatMessageStat(
        total_messages_count=len(chat.messages),
        total_words_count=total_words,
        user_stats=user_stats)