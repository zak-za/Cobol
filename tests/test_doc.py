""" Test word doc """

import os
from src.document import Document


def test_create_doc():
    """test create document"""

    doc = Document()
    doc.add_heading("TEST", level=1)
    doc.save_document("test_create_document")
    assert os.path.isfile(os.getcwd() + "/out/test_create_document.docx")


def test_add_paragraph():
    """test add paragraphe to document"""

    doc = Document()
    doc.add_heading("TEST", level=1)
    parag = doc.add_paragraphe()
    parag.add_run("TEST")
    doc.save_document("test_para_document")
    assert os.path.isfile(os.getcwd() + "/out/test_para_document.docx")
