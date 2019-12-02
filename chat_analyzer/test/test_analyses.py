from collections import namedtuple
from datetime import datetime

import pytest

from chat_analyzer.analysis.words_finder import get_top_used_words
from chat_analyzer.models.chat_data import Chat, Message


class TestAnalyses:
    NAME_A = "Alice"
    NAME_B = "Bob"

    FREQ_A = [20, 18, 16, 14, 12, 10, 8, 6, 4, 2]
    FREQ_B = [19, 17, 15, 13, 11, 9, 7, 5, 3, 1]

    InputData = namedtuple("TestData", ["limit", "length"])
    Expected = namedtuple("Expected", ["rank"])

    _WORD_RANK_DATA = [
        (InputData(limit=1, length=1), Expected(rank=[("a", 20)])),
        (InputData(limit=3, length=1), Expected([("a", 20), ("b", 19), ("aa", 18)])),
        (InputData(limit=5, length=5), Expected([("aaaaa", 12), ("bbbbb", 11), ("aaaaaa", 10), ("bbbbbb", 9), ("aaaaaaa", 8)])),
        (InputData(limit=10, length=10), Expected([("aaaaaaaaaa", 2), ("bbbbbbbbbb", 1)])),
        (InputData(limit=10, length=99), Expected([])),
    ]

    @pytest.mark.parametrize("test_input, expected", _WORD_RANK_DATA)
    def test_word_rank(self, test_input: InputData, expected: Expected):
        chat = self._get_test_chat()
        rank = get_top_used_words(chat, test_input.limit, test_input.length)

        assert rank is not None
        assert len(rank) == len(expected.rank)
        assert rank == expected.rank

    def _get_test_chat(self) -> Chat:

        messages_a = []
        messages_b = []
        dt = datetime.now()

        for i in range(10):
            a_word = ""
            b_word = ""

            # Creates f+1 length "aaa..." and "bbb..." sequences
            for _ in range(i + 1):
                a_word = a_word + "a"
                b_word = b_word + "b"

            a_sentence = " ".join([a_word for _ in range(self.FREQ_A[i])])
            b_sentence = " ".join([b_word for _ in range(self.FREQ_B[i])])

            messages_a.append(Message(self.NAME_A, dt, a_sentence))
            messages_b.append(Message(self.NAME_B, dt, b_sentence))

        return Chat("TestChat", [self.NAME_A, self.NAME_B], messages_a + messages_b)
