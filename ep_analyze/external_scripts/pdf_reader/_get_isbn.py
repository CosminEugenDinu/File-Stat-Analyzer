import os, io, re
import fitz
from PIL import Image, ImageEnhance
from pytesseract import image_to_string


def get_isbn(pdf_path, pgs_to_search):
    
    # if not os.path.isfile(pdf_path):
    #     return 'no file'

    isbn_re = re.compile(r'i\s*?s\s*?b\s*?n\s*?.{0,30}', re.I)

    doc = fitz.open(pdf_path)
    max_num_pages = pgs_to_search 

    # read first 10 pages
    # for i in range(doc.pageCount+1):
    #     if i > 10: break
        # page = doc.loadPage(i)
    count = -1
    for page in doc: 
        count += 1
        if count >= max_num_pages: break

        text = page.getText()
        if isbn_like := isbn_re.search(text):
            found_at_page = count 
            return isbn_like.group(), found_at_page

    # if isbn not found, get images
    
    # for i in range(doc.pageCount+1):
    #     if i > 10: break
    #     page = doc.loadPage(i)
    
    count = -1
    for page in doc:
        count += 1
        if count > max_num_pages: break

        t_page = page.getTextPage(4)
        d_page = t_page.extractDICT()
        for block in d_page['blocks']:
            # if block is type image
            if block['type'] == 1:
                # open byte file in memory (buffer)
                buffer = io.BytesIO()
                # write image bytes to buffer
                buffer.write(block['image'])
                buffer.seek(0)

                # open buffer image file in PIL.Image
                im = Image.open(buffer)
                im = im.convert("L")
                im = ImageEnhance.Contrast(im)
                im = im.enhance(3)

                # convert image to string with pytesseract.image_to_string
                text_img = image_to_string(im)

                if isbn_like := isbn_re.search(text_img):
                    buffer.close()
                    found_at_page = count 
                    return isbn_like.group(), found_at_page

                buffer.close()
    return 'isbn_not_found', 'no_page' 
