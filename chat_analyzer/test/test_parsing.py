from datetime import datetime

import chat_analyzer.parsing.parser as parser


class TestParser:
    def test_parsing_no_file(self):
        file_path = "test_files/not_exist_file.txt"
        try:
            parser.parse_chat(file_path)
            assert False, "missing file should raise an exception"
        except FileNotFoundError:
            assert True

    def test_parsing_no_file_multiple(self):
        file_paths = [
            "test_files/chat_simple.txt",
            "test_files/not_exist_file.txt",
        ]

        try:
            parser.parse_chat_multiple(file_paths)
            assert False, "missing files should raise an exception"
        except FileNotFoundError:
            assert True

    def test_parser(self):
        chat = parser.parse_chat("test_files/chat_simple.txt")

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



