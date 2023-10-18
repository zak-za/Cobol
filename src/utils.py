""" Declare Helpers """

from fnmatch import translate
import re
import time
import requests
from src.constants import KEY_WORDS, SPECIAL_KEY_WORDS
from src.config import ENCODING
from src.document import Document
from src.translate import translate, handle_header


def init_document() -> Document:
    """Initialize document object

    Returns:
        Document
    """

    doc = Document()
    doc.add_heading(header="Descripción Funcional Detallada", level=1)
    paragraphe = doc.add_paragraphe(
        "BREVE DESCRIPCIÓN FUNCIONAL DEL PROGRAMA.")
    paragraphe.bold = True
    doc.add_paragraphe("Genera fichero de recibos para TIREA.")
    paragraphe = doc.add_paragraphe("DESCRIPCIÓN TÉCNICA DEL PROGRAMA")
    paragraphe.bold = True

    return doc


def handle_special_key_words(doc, file, line, word) -> str:
    """handle special key words

    Args:
        file (file)
        line (str)
        word (str)

    Returns:
        str
    """
    next_line = line
    temp = next_line
    break_point = "END-" + word

    while True:
        next_line = file.readline()
        clean_next_line = clean_line(line=next_line)
        temp += " <br /> " + clean_line(line=next_line)
        if word == "MOVE":
            if clean_next_line.strip() == "":
                continue
            elif clean_next_line.startswith("TO"):
                temp += " " + clean_next_line
            elif not clean_next_line.startswith("MOVE"):
                break
            translate(doc=doc, word=word, line=temp)
            temp = clean_line(next_line)
        elif break_point in next_line:
            break

    return temp


def clean_line(line: str = "") -> str:
    """_summary_

    Args:
        line (str, optional): Defaults to "".

    Returns:
        str
    """

    line = line.lstrip("0123456789").strip(" *\n")
    line = re.sub(r"\d+\.\d+\.\d+", "", line).strip().lstrip()
    return line


def is_key_word(word: str) -> bool:
    """Check if word is in key words liste

    Args:
        word (str)

    Returns:
        bool
    """

    if word in KEY_WORDS:
        return True
    return False


def is_special_keyword(word: str) -> bool:
    """Check if word is treated as special keyword

    Args:
        word (str)

    Returns:
        bool
    """

    if word in SPECIAL_KEY_WORDS:
        return True
    return False


def is_perform(word: str) -> bool:
    """Check if word is equal to perform

    Args:
        word (str)

    Returns:
        bool
    """

    if word.lower() == "perform":
        return True
    return False


def get_procedure_division(file_path: str) -> list:
    """get procedure division

    Args:
        file_path (str)

    Returns:
        list
    """
    performs = []

    with open(file_path, mode="r", encoding=ENCODING) as file:
        while True:
            line = file.readline()
            if not line:
                break
            line = clean_line(line=line)
            words = line.split()
            if len(words):
                if is_perform(word=words[0]):
                    temp = line.split()
                    if len(temp):
                        word_to_save = (
                            temp[1] + "."
                            if temp[1][len(temp[1]) - 1] != "."
                            else temp[1]
                        )
                        performs.append(word_to_save)
    return performs


def download_input_file(file_url: str) -> str:
    """download input file

    Args:
        file_url (str)

    Returns:
        str
    """

    response = requests.get(file_url, allow_redirects=True)
    file_name = f"in/in_{time.strftime('%Y%m%d_%H%M%S')}.txt"
    open(file_name, 'wb').write(response.content)
    return file_name
