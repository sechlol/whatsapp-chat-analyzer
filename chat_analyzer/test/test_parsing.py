import os
from datetime import datetime

import chat_analyzer.parsing.parser as parser

def _get_path(relative_file_path: str) -> str:
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    return os.path.join(current_directory, relative_file_path)

class TestParser:
    def test_parsing_no_file(self):
        file_path = _get_path("test_files/not_exist_file.txt")
        try:
            parser.parse_chat(file_path)
            assert False, "missing file should raise an exception"
        except FileNotFoundError:
            assert True

    def test_parsing_no_file_multiple(self):
        file_paths = [
            _get_path("test_files/chat_simple.txt"),
            _get_path("test_files/not_exist_file.txt"),
        ]

        try:
            parser.parse_chat_multiple(file_paths)
            assert False, "missing files should raise an exception"
        except FileNotFoundError:
            assert True

    def test_parser(self):
        chat = parser.parse_chat(_get_path("test_files/chat_simple.txt"))

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



