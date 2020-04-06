from ep_analyze.models import FileStat
from ep_analyze.scripts.file_stat import FileStatReader

from ep_analyze.scripts.tests.particular_tests import test_FileStat_re_pattern

from django.test import TestCase
from django.db import connection
from django.utils import timezone

from dev_tools.messages import Messages

import sys, re, io
from time import time
from datetime import datetime

sys.stderr.write(f'[{__name__}]\n')

fsr = FileStatReader()

# test re pattern
try:
    # msg = test_FileStat_re_pattern('v1')
    # msg = test_FileStat_re_pattern('v')
    msg = test_FileStat_re_pattern()
    msg != [] and sys.stderr.write(str(msg))
except AssertionError as e:
    sys.stderr.write(str(e))

test_src_file_stat = 'ep_analyze/scripts/tests/test_src_file_stat'
src_file_stat = 'ep_analyze/ep_files_stat/find_all_stat'


class FileStatStreamToTableTest(TestCase):

    def setUp(self):
        # test for database errors
        fsr.filestream_to_table(src_file_stat, FileStat)
    
    def test_FileStat_model(self):
        pass





