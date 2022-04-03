
from cgitb import text


def character_escape(text: str) -> str:
    modified_text = ""
    for char in text:
        if char == "'":
            char = "''"
        modified_text += char
    return modified_text