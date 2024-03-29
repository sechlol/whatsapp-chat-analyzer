import re
from typing import List, Tuple, Optional
from chat_analyzer.models.chat_data import Chat, Message


def find_messages_with_words(word_list: List[str], chat: Chat) -> List[Message]:
    return [m for m in chat.messages if _contains_word(word_list, m)]


def find_messages_without_words(word_list: List[str], chat: Chat) -> List[Message]:
    return [m for m in chat.messages if not _contains_word(word_list, m)]


def get_top_used_words(chat: Chat, limit: int = 10, min_length: int = 4, **kwargs) -> List[Tuple[str, int]]:
    """ Return a list of the most used words with their number of occurrences, in descending order """
    sorted_words = _get_sorted_words(chat)

    i = count = 0
    top_words = []
    limit = min(limit, len(sorted_words))
    while i < len(sorted_words) and count < limit:
        if len(sorted_words[i][0]) >= min_length:
            top_words.append(sorted_words[i])
            count += 1
        i += 1

    return top_words


def _contains_word(word_list: List[str], message: Message) -> bool:
    return re.search(r'\b' + '|'.join(word_list) + r'\b', message.text, flags=re.IGNORECASE) is not None


def get_word_rank(chat: Chat, word: str) -> Optional[Tuple[int, int]]:
    """ Returns the ranking of the word (1st) with the number of occurrences in the chat (2nd) """
    words = _get_sorted_words(chat)
    rank = 0
    word_lower = word.lower()
    for word_item in words:
        rank += 1
        if word_item[0] == word_lower:
            return rank, word_item[1]

    return None


def _get_sorted_words(chat: Chat) -> List[Tuple[str, int]]:
    """ Each element in the list is a word with its number of occurrences in the chat """
    words = dict()
    rgx = re.compile(r"(\w[\w']*\w|\w)", flags=re.IGNORECASE)
    for m in chat.messages:
        text = m.text.replace("Media omitted", "")
        for word in rgx.findall(text):
            word_lower = word.lower()
            words[word_lower] = words.get(word_lower, 0) + 1

    return sorted(words.items(), key=lambda kv: -kv[1])
