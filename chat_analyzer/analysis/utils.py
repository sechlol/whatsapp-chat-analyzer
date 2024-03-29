import re
from typing import List


def get_words_from_text(text: str) -> List[str]:
    return re.findall("(\w[\w']*\w|\w)", text, flags=re.IGNORECASE)