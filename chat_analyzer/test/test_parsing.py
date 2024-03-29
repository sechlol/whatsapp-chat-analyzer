from datetime import datetime

import pytest

import chat_analyzer.parsing.parser as parser
from chat_analyzer.models.app_data import AppArgs
from chat_analyzer.test.utils import get_test_path


class TestParser:
    def test_parsing_no_file(self):
        file_path = get_test_path("not_exist_file.txt")
        args = AppArgs(file_path, "", None, [])
        with pytest.raises(Exception):
            parser.load(args)

    def test_parsing_wildcard(self):
        file_path = get_test_path("chat_simple_*.txt")
        args = AppArgs(file_path, "", None, [])
        chats = parser.load(args)
        assert len(chats) == 2

    def test_parser(self):
        file_path = get_test_path("chat_simple_1.txt")
        args = AppArgs(file_path, "", None, [])
        chats = parser.load(args)
        assert len(chats) == 1

        chat = chats[0]
        assert len(chat.participants) == 3
        assert len(chat.messages) == 3

        assert chat.participants[0] == "User One"
        assert chat.participants[1] == "User Two"
        assert chat.participants[2] == "User 3"

        assert chat.messages[0].date == datetime(2019, 11, 24, 12, 1)
        assert chat.messages[0].text == "Lorem"
        assert chat.messages[0].sender == "User One"

        assert "ਡ" in chat.messages[1].text
        assert chat.messages[2].text == "dolor sit amet"
