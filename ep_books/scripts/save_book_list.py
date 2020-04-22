import csv
from django.apps import apps
from ..models import Document
from tabulate import tabulate
from pprint import pprint



def save_books_info():

    FileStat = apps.get_model('ep_analyze', 'FileStat')
    Doc2Files = Document.files.through


    all_books = Document.objects.values()

    first_book = all_books[0]

    file = Doc2Files.objects.get(document_id=first_book['id'])
    fn = FileStat.objects.get(id=file.filestat_id).name
    # print(fn)
    # pprint(all_books[0]['google_isbn_info'])


    csv_rows = [('pages', 'title', 'authors', 'preview', 'more')]


    for b in all_books:
        if items := b['google_isbn_info'].get('items'):
            if len(items)>0:
                pages = items[0]['volumeInfo'].get('pageCount')
                title = items[0]['volumeInfo']['title']
                authors = items[0]['volumeInfo'].get('authors')
                preview = items[0]['volumeInfo'].get('previewLink')
                more = items[0]['volumeInfo'].get('infoLink')
                csv_rows.append((pages, title, authors, preview, more))
    
    with open('books_info.csv', 'w', newline='') as csv_file:
        csv_w = csv.writer(csv_file, delimiter='\t')
        csv_w.writerows(csv_rows)


save_books_info()

def run():
    pass