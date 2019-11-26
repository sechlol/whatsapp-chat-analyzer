import glob
import ntpath
import os
from typing import List, Optional

from chat_analyzer.models.chat_data import Chat
from chat_analyzer.parsing.whatsapp_parser import parse_whatsapp_file


def load(path_pattern) -> Optional[List[Chat]]:
    chats = [_parse_chat(file) for file in glob.glob(path_pattern)]
    if len(chats) == 0:
        raise Exception("No files found.")
    return chats


def _parse_chat(path: str) -> Chat:
    return parse_whatsapp_file(_read_json(path), _get_filename(path))


def _get_filename(path: str) -> str:
    """ Return the filename (without extension) given a path"""
    head, tail = ntpath.split(path)
    name_and_ext = tail or ntpath.basename(head)
    name, ext = os.path.splitext(name_and_ext)
    return name


def _read_json(file_name: str) -> List[str]:
    with open(file_name, mode='r', encoding="utf8") as file:
        return file.readlines()
