from ep_analyze.models import FileStat
from ep_analyze.models import Dummy
from ep_analyze.scripts.file_stat import FileStatReader

from ep_analyze.scripts.particular_tests import test_FileStat_re_pattern

from django.test import TestCase
from dev_tools.messages import Messages
import sys

sys.stderr.write('test')

fsr = FileStatReader()

# src_file_stat = 'ep_analyze/ep_files_stat/test_src_file'
src_file_stat = 'ep_analyze/ep_files_stat/find_all_stat'


fsr.file_to_table(src_file_stat, FileStat)





# msg = test_FileStat_re_pattern()
# sys.stderr.write(str(msg))