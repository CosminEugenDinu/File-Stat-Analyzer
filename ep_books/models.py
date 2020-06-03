from django.db import models
from django.contrib.postgres.fields import JSONField
from ep_analyze.models import FileStat


class Document(models.Model):

    files = models.ManyToManyField(FileStat)

    isbn = models.CharField(max_length=13)

    google_isbn_info = JSONField() 



class FileContentInfo(models.Model):
    """
    Files content analyze.
    """
    file_id = models.ForeignKey(FileStat, on_delete=models.CASCADE)

    # like "pymupdf getText"
    read_method = models.CharField(max_length=50)

    # array of pages, like [0, 1, 2, 5] or [1-10, 15-30]
    pages_inspected = models.CharField(max_length=1000)

    # array of found page dimensions, like {"330.53,33.23":[0, 1, 3]} 
    pages_dimensions = JSONField()

    dimension_unit = models.CharField(max_length=20)
    
    # found isbn like text
    isbn_like = models.CharField(max_length=20)

    # cleaned isbn
    isbn = models.CharField(max_length=13)

    # num of page at which isbn text was found
    pages_with_isbn = models.CharField(max_length=50)

    # total num of characters found in inspected pages key:page, value:num_of_chars
    page_chars = JSONField()

    # total num of images found in inspected pages
    page_images = JSONField() 
    
    # total num of pages of whole document
    doc_pagecount = models.IntegerField()
    