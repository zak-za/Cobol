""" Run project """

from src.translate import translate, handle_header
from src.utils import (
    init_document,
    clean_line,
    handle_special_key_words,
    is_key_word,
    is_special_keyword,
    get_procedure_division,
    download_input_file
)
from src.config import ENCODING


def main(file_path, doc):
    """Read file and performe line by line

    Args:
        args (Array): array of strings
        doc (Document)
    """

    procedure_division = get_procedure_division(file_path=file_path)
    #tmp=[["phrase","1"],["gaga","2"],["papap","3"]]
    #doc.add_table(data=tmp, rows=len(tmp), cols=2)

    with open(file_path, mode="r", encoding=ENCODING) as file:
        while True:
            line = file.readline()
            if not line:
                break

            # ------------------------------------ process current line
            try:
                line = clean_line(line=line)
                words = line.split()
                if len(words):
                    word = words[0]
                    # -------------- handle headers
                    if word in procedure_division:
                        doc.add_paragraphe(handle_header(line))
                        #print(f"------------------ {line}")
                    # --------------- handle others
                    else:
                        if is_key_word(word=word):
                            if is_special_keyword(word=word):
                                line = handle_special_key_words(
                                    doc=doc, file=file, line=line, word=word
                                )
                            #print('what :'+f"{line}")
                            word = line.split()[0]
                            translate(doc=doc, word=word, line=line)
            except Exception as ex:
                print("line;;;", line)
                print(f"!!!!!!!!!!! Error processing : {ex}")
                continue


def run_batch(file_url, doc):
    """Online file

    Args:
        args (Array): : array of strings
        doc (Document)
    """

    file_path = download_input_file(file_url=file_url)
    main(file_path=file_path, doc=doc)


def run_stream(file_path, doc):
    """local file

    Args:
        args (Array): : array of strings
        doc (Document)
    """
    main(file_path=file_path, doc=doc)


def run(args):
    """Run the program

    Args:
        args (Array): : array of strings
    """

    doc = init_document()

    if args[1].startswith('http'):
        run_batch(file_url=args[1], doc=doc)
    else:
        run_stream(file_path=args[1], doc=doc)

    doc.save_document()
