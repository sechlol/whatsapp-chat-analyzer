from enum import Enum
from typing import List

from chat_analyzer.analysis.chat_messages_count import messages_per_user_count
from chat_analyzer.analysis.chat_time_stats import messages_per_day_count, initiation_score_per_interval, \
    chat_engagement
from chat_analyzer.analysis.words_finder import get_top_used_words
from chat_analyzer.models.chat_data import Chat


class AnalysisType(Enum):
    MESSAGES_COUNT = 1
    MESSAGES_PER_DAY = 2
    WORDS_MOST_USED = 3

    INITIATION_SCORES = 4
    ENGAGEMENT_SCORE = 5


def analyze(mode: AnalysisType, chats: List[Chat], **kwargs):
    if mode == AnalysisType.MESSAGES_COUNT:
        return [messages_per_user_count(chat=chat) for chat in chats]

    if mode == AnalysisType.MESSAGES_PER_DAY:
        return [messages_per_day_count(chat=chat) for chat in chats]

    if mode == AnalysisType.WORDS_MOST_USED:
        return [get_top_used_words(chat=chat, **kwargs) for chat in chats]

    if mode == AnalysisType.INITIATION_SCORES:
        if "hour_interval" not in kwargs:
            raise Exception(f"Mode {mode.name} requires parameter hour_interval [int]")
        return [initiation_score_per_interval(chat=chat, **kwargs) for chat in chats]

    if mode == AnalysisType.ENGAGEMENT_SCORE:
        if "subject" not in kwargs:
            raise Exception(f"Mode {mode.name} requires parameter subject [string]")
        return chat_engagement(chats=chats, **kwargs)