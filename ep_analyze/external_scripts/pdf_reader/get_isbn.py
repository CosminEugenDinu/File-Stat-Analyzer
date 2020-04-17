
import os, io, re
import fitz
from PIL import Image, ImageEnhance
from pytesseract import image_to_string


def get_isbn(pdf_path, pgs_to_search):

    isbn_re = re.compile(r'i\s*?s\s*?b\s*?n\s*?.{0,30}', re.I)

    doc = fitz.open(pdf_path)
    max_num_pages = pgs_to_search 

    count = -1
    for page in doc: 
        count += 1
        if count >= max_num_pages: break

        text = page.getText()
        if isbn_like := isbn_re.search(text):
            found_at_page = count 
            return isbn_like.group(), found_at_page
   

    return 'isbn_not_found', 'no_page' 
