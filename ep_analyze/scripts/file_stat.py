import os
import re
import sys
from time import time
from django.apps import apps

# linux command:
# $ find . -exec stat -c "%F %s %X %Y %n" {} \; > file
# %F=fileType %s=totalSizeBytes %X=lastAccess %Y=lastModification %n=fileName

# actual linux command:
# sudo find /mnt \( -path '*/c' -o -path '*/System\ Volume\ Information' \) -prune -o -name '*' -exec stat -c "%F %s %X %Y %n" {} + > /home/cos/find_all_stat`

class FileStatReader:

    def __init__(self):

        self.server_name = ''
        self.server_addr = ''

        # self.files_stat = {
        #     # index of record
        #     'i': [],
        #     # list of booleans, True for file, False for directory
        #     'is_files' : [],
        #     # str digits = size in bytes
        #     'sizes': [],
        #     # str digits = last accessed time in seconds from epoch
        #     'acc_times': [],
        #     # str digits = last modified time in seconds from epoch
        #     'mod_times': [],
        #     # path like '/mnt/d' with depth=2
        #     'root_dir_paths': [],
        #     # path like '/maindir/subdir/lastdir/'
        #     'parent_dir_paths': [],
        #     # name of file from storage, end of path after '/', including extension
        #     'file_names': [],
        #     # found suffix at end of file_name, after '.'; can be extension like '.pdf'
        #     'suffixes': []
        # }

    def _file_re_pattern(self):
        """
        Test online here https://pythex.org/
        """
        # `stat -c "%F %s %X %Y %n" <file>` linux bash command
        # match 'file' or 'directory'
        _type = '(?:regular |)(?:empty |)(file|directory)\s'
        size = acc_time = mod_time = r'(\d+)\s'
        # match path like /path/to/parent_dir/ 
        parent_dir_path = r'(\.?\/.*\/|)\/?'
        # name returns [full_file_name, .ext or '']
        name = r'(\.?[^/]*?(\.\w{1,10}$|$))'

        return f'{_type}{size}{acc_time}{mod_time}{parent_dir_path}{name}'
    
    def file_to_table(self, stat_file_path, model):
        """
        Read source stat file, match patterns (fields) and insert to
        corresponding table (model) in database line by line
        """
        pat_str = self._file_re_pattern()
        pat_bytes = pat_str.encode()

        s_regex = re.compile(pat_str)
        b_regex = re.compile(pat_bytes)
        

        print('.'*10+'file_to_table test'+'.'*10)
        lines_traveled = 0
        lines_matched = 0
        with open(stat_file_path, 'rb') as bytes_reader:
            t1 = time()
            for line in bytes_reader:
                lines_traveled += 1
                if m := b_regex.match(line):
                    lines_matched += 1
                    # print(m.groups())
            t2 = time()
        delta1 = t2 - t1
        print(f'{lines_traveled}/{lines_matched} lines matched')
        print('bytes read took', delta1)

        lines_traveled = 0
        lines_matched = 0
        lines_not_matched = []

        with open(stat_file_path, 'r') as str_reader:
            t3 = time()
            for line in str_reader:
                lines_traveled += 1
                if m := s_regex.match(line):
                    lines_matched += 1
                else:
                    lines_not_matched.append(lines_traveled)

            t4 = time()
        delta2= t4 - t3
        print(f'{lines_traveled}/{lines_matched} lines matched')
        print('string read took', delta2)
        print('lines not matched', lines_not_matched)




    # def load_file(self, file_path, limit=2):

    #     # source_file_name = re.compile(r'.*\/([^/]*)$').match(file_path).group(1)

    #     file_stat_re = re.compile(self._file_re_pattern())

    #     with open(file_path) as file_reader:
    #         i = 1
    #         for line in file_reader:
    #             # limit for testing
    #             if i >= limit: break;

    #             if m := file_stat_re.match(line):
    #                 size, acc_time, mod_time, _,\
    #                 parent_dir_path, name, suffix = m.groups()

    #                 self.files_stat['i'].append(i)
    #                 self.files_stat['sizes'].append(size)
    #                 self.files_stat['acc_times'].append(acc_time)
    #                 self.files_stat['mod_times'].append(mod_time)
    #                 self.files_stat['parent_dir_paths'].append(parent_dir_path)
    #                 self.files_stat['file_names'].append(name)
    #                 self.files_stat['suffixes'].append(suffix)
    #                 i += 1
    
    def suffixes(self):
        suf_dict = {}

        for suf in self.files_stat['suffixes']:
            if s := suf_dict.get(suf):
                suf_dict[suf] += 1
            else:
                suf_dict[suf] = 1

        return suf_dict

    def pdf_s_ids(self):
        """
        Returns a list with idx from self.files_stat where suffix is .pdf or .PDF
        """
        pdf_s_list = []

        for i, pdf_suf in enumerate(self.files_stat['suffixes']):
            pdf_match = re.compile(r'^.pdf$', flags=re.I).match(pdf_suf)
            if pdf_match:
                pdf_s_list.append(i)

        return pdf_s_list
    
    def pdf_sizes_ids(self):
        """
        Return pdf_s sizes, unique (id) and same (ids).
        dict same_size: key: size_str, value: [ids_int]
        dict unique_sizes: key: size_str, value: id_int
        id_int from self.files_stat['i']
        """
        sizes = {
            'same_sizes': {},
            'unique_sizes': {}
        }

        pdf_s_ids = self.pdf_s_ids()

        for i in pdf_s_ids:
            # if id > 10000: break;

            file_name = self.files_stat['file_names'][i]
            size = self.files_stat['sizes'][i]

            if ss := sizes['same_sizes'].get(size):
                ss.append(i)
            elif us_id := sizes['unique_sizes'].get(size):
                sizes['same_sizes'][size] = [us_id, i]
                del sizes['unique_sizes'][size]
            else:
                sizes['unique_sizes'][size] = i

        return sizes
    
    def pdf_same_sizes_names(self):
        """
        Iterates through lists of same size pdf_s and get only the first occurrence as file_name.
        Returns list of pdf_s file_names.
        """
        pdf_names = []



        return pdf_names

    def pdf_unique_sizes_names(self):
        """
        Return list of pdf file_names with unique sizes.
        """
        pdf_names = []

        return pdf_names

app_path = apps.get_app_config('ep_analyze').path
files_stat_path = os.path.join(app_path, 'ep_files_stat')

source_file_path = os.path.join(files_stat_path, 'find_all_stat')


# FS = FileStat()
# print('eat file begin:', t1:=time())
# FS.eat_file(drive_stat_path)
# print('eat file end', t2:=time())
# print('total time:', t2 - t1)

# def test():
#     FS = FileStat()
#     FS.re_pattern = file_re_pattern()
#     FS.eat_file(drive_stat_path)
#     FS.eat_file(comenzi_1_stat_path)
#     FS.eat_file(comenzi_2_stat_path)
#     FS.eat_file(comenzi_3_stat_path)

# if __name__=='__main__':
#     from timeit import Timer
#     t = Timer("test()", "from __main__ import test")
#     print('eat files took:', t.timeit(2))