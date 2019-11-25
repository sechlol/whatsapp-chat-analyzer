import re
from datetime import datetime
from typing import List

from chat_analyzer.models.chat_data import Chat, Message


def parse_whatsapp_file(chat_file: List[str]) -> Chat:
    chat = Chat()
    last_message = None

    for line in chat_file:
        match = re.search(r'^(\d+)/(\d+)/(\d+), (\d+):(\d+) - ([^:]+): (.+)$', line)
        if match:
            month = int(match.group(1))
            day = int(match.group(2))
            year = int(match.group(3)) + 2000
            hour = int(match.group(4))
            minute = int(match.group(5))

            last_message = Message(
                date=datetime(year=year, month=month, day=day, hour=hour, minute=minute),
                sender=match.group(6),
                text=match.group(7).rstrip())

            chat.add_message(last_message)

        elif last_message:
            # these are messages that contain text with newlines. Append them to the previous message
            # last_message.text = last_message.text.replace("/n", " ") + line
            last_message.text = f"{last_message.text} {line.rstrip()}"

    return chat
