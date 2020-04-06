from .file_stat import FileStatReader
from ..models import FileStat as FileStatModel  

src_file_stat = 'ep_analyze/ep_files_stat/find_all_stat'

file_stat_reader = FileStatReader()

def run():

    file_stat_reader.filestream_to_table(src_file_stat, FileStatModel)

