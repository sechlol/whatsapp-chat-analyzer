from typing import List

from chat_analyzer.models.chat_data import Chat
from chat_analyzer.parsing.io_utils import read_json
from chat_analyzer.parsing.whatsapp_parser import parse_whatsapp_file


def parse_chat(path: str) -> Chat:
    return parse_whatsapp_file(read_json(path))


def parse_chat_multiple(paths: List[str]) -> List[Chat]:
    return [parse_chat(path) for path in paths]
