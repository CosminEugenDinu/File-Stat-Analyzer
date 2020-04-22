import requests
from ..models import Document



def isbn_search(isbn):
    url = 'https://www.googleapis.com/books/v1/volumes'
    params = {"q": isbn}
    re = requests.get(url, params=params)
    re_dict = re.json()    
#    print(dir(re))
#    print(dir(json))
#    print(re.status_code)
    # print(re_dict['items'][0]['volumeInfo']['title'])
    # print(re_dict['items'][0]['volumeInfo'])
    return re_dict

# isbn_search(isbn)

 
# h = {'X-API-Key': 'YOUR_REST_KEY'}
# resp = requests.get("https://api.isbndb.com/book/9781934759486", headers=h)
# print(resp.json())

def resolve_isbn():

    doc_all = Document.objects.all()

    for doc in doc_all:

        doc.google_isbn_info = isbn_search(doc.isbn)
        doc.save()
    

def run():
    pass