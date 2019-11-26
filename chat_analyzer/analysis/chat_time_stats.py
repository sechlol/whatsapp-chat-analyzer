from datetime import datetime, timedelta, date
from typing import Dict, List

from chat_analyzer.models.chat_data import Chat, StatsWrapper, MessagesPerDayStat, Score


def messages_per_day_count(chat: Chat) -> StatsWrapper:
    days = dict()

    for message in chat.messages:
        date_sent = message.date.date()
        if date_sent not in days:
            days[date_sent] = dict()

        current_count = days[date_sent].get(message.sender, 0)
        days[date_sent][message.sender] = current_count + 1

    return _sort_and_format_messages_per_date(days)


def chat_engagement(chats: List[Chat], subject: str, **kwargs) -> StatsWrapper:
    engagement = dict()

    for chat in chats:
        if subject not in chat.participants:
            continue

        participants = chat.participants[:]
        participants.remove(subject)

        for message in chat.messages:
            if message.sender != subject:
                continue

            date_sent = message.date.date()
            if date_sent not in engagement:
                engagement[date_sent] = {}

            sent_count = engagement[date_sent].get(chat.name, 0)
            engagement[date_sent][chat.name] = sent_count + 1

    return _sort_and_format_messages_per_date(engagement)


def initiation_score_per_day(chat: Chat) -> StatsWrapper:
    last_date = None
    initiation = []
    scores = {name: 0 for name in chat.participants}
    for message in chat.messages:
        if message.date.date() == last_date:
            continue

        last_date = message.date.date()
        scores[message.sender] += 1

        initiation.append(MessagesPerDayStat(
            date_sent=last_date,
            scores=[Score(label=kv[0], value=kv[1]) for kv in scores.items()],
        ))

    return StatsWrapper(legend=chat.participants, stats=initiation)


def initiation_score_per_interval(chat: Chat, hour_interval: int, **kwargs) -> StatsWrapper:
    last_date = datetime.min
    initiation = []
    scores = {name: 0 for name in chat.participants}
    for message in chat.messages:
        if message.date >= last_date + timedelta(hours=hour_interval):
            scores[message.sender] += 1
            initiation.append(MessagesPerDayStat(
                date_sent=message.date,
                scores=[Score(label=kv[0], value=kv[1]) for kv in scores.items()],
            ))
        last_date = message.date

    return StatsWrapper(legend=chat.participants, stats=initiation)


def _sort_and_format_messages_per_date(scores_per_date: Dict[date, Dict[str, int]]) -> StatsWrapper:
    # sort items per date and place them in a list
    sorted_pairs = sorted(scores_per_date.items(), key=lambda kv: kv[0])
    stats = []
    legend = set()
    for (date_sent, scores) in sorted_pairs:
        legend = legend.union(scores.keys())
        stats.append(
            MessagesPerDayStat(
                date_sent=date_sent,
                scores=[Score(label=score[0], value=score[1]) for score in scores.items()]
            )
        )
    return StatsWrapper(legend=list(legend), stats=stats)
