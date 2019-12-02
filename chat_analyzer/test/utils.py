import os
import random

from datetime import datetime, timedelta
from random import randint
from typing import List

from random_words import RandomNicknames, LoremIpsum
from chat_analyzer.models.chat_data import Chat, Message


def get_test_path(relative_file_path: str) -> str:
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, "test_files/" + relative_file_path)


def generate_random_chat(message_count: int, participants: int = 2) -> Chat:
    return generate_random_chats(message_count, participants)[0]


def generate_random_chats(message_count: int, participants: int = 2, chats_number: int = 1) -> List[Chat]:
    rn = RandomNicknames()
    li = LoremIpsum()
    chats = []

    # Weighted sentence length probability table
    message_length_probability = \
        [1] * 25 + \
        [2] * 35 + \
        [3] * 20 + \
        [4] * 10 + \
        [5] * 7 + \
        [6] * 3

    for chat_n in range(chats_number):
        people = rn.random_nicks(count=participants)
        dt = datetime.now()
        messages = []

        for i in range(message_count):
            # Generate random time intervals between 10 seconds and 24 hours
            secs = randint(10, 60 * 60 * 24)
            dt = dt + timedelta(seconds=secs)

            # chooses a random sender
            sender = random.choice(people)

            # generate random message:
            sentences_number = random.choice(message_length_probability)
            text = li.get_sentences(sentences_number)

            messages.append(Message(sender, dt, text))

        chats.append(Chat(f"RandomChat_{chat_n}", people, messages))

    return chats
