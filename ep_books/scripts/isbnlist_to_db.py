import os, re, csv
from collections import defaultdict
from django.apps import apps
from django.db.models import Q
from ..models import Document

from tabulate import tabulate



app_path = apps.get_app_config('ep_analyze').path
isbnlist_path = os.path.join(app_path, 'ep_isbnlists', 'isbnlist.csv')

print('.............................................................')

isbn_table = defaultdict(list)
isbn_like_table = defaultdict(list)

isbn_re = re.compile(r'ISBN\D*(?:13|10|..?.\))?\D*((?:\d+.?){4,5}|\d{10}|\d{13})\s*', re.I)

FileStat = apps.get_model('ep_analyze', 'FileStat')

class Files():
    def __init__(self, FileStatModel):
        self.FileStatModel = FileStatModel
        self.files_all = FileStatModel.objects.values()
    
    def find_by_path(self, path):
        dir, name = re.match(r'(.*\/)(.*)', path).groups()
        for file in self.files_all:
            if file['parent_dir_path'] == dir and file['name'] == name:
                return file

files = Files(FileStat)

# list with instances of Document model
documents = []
# list with instances of "through" model of files m2m of Document
doc_files_m2m = []

with open(isbnlist_path, 'r', newline='') as isbnlist_csv:
    csv_r = csv.reader(isbnlist_csv, delimiter='\t')

    if last_doc := Document.objects.last():
        doc_id = last_doc.id
    else:
        doc_id = 0

    for row in csv_r:
        doc_id += 1

        file_id = files.find_by_path(row[0])['id']

        if m := isbn_re.match(row[1]):
            isbn1 = m.groups()[0]
            isbn2 = re.sub('\D', '', isbn1)
            if len(isbn2) == 10 or len(isbn2) == 13:
                d = Document()
                d.id = doc_id
                d.isbn = isbn2
                d.google_isbn_info = {}
                f = Document.files.through(document_id=doc_id, filestat_id=file_id)
                documents.append(d)
                doc_files_m2m.append(f)

def save_documents():
    """
    Saves documents to db
    """
    Document.objects.bulk_create(documents)
    Document.files.through.objects.bulk_create(doc_files_m2m)


def run():
    pass