import os
import re
from time import time
from django.apps import apps

# linux command:
# $ find . -exec stat -c "%F %s %X %Y %n" {} \; > file
# %F=fileType %s=totalSizeBytes %X=lastAccess %Y=lastModification %n=fileName

# actual linux command:
# sudo find /mnt \( -path '*/c' -o -path '*/System\ Volume\ Information' \) -prune -o -name '*' -exec stat -c "%F %s %X %Y %n" {} + > /home/cos/find_all_stat`

class FileStat:

    def __init__(self):

        self.server_name = ''
        self.server_addr = ''
        # name of source file with data
        self.source_file_name = '' 

        self.files_stat = {
            # index of record
            'i': [],
            # list of booleans, True for file, False for directory
            'is_files' : [],
            # str digits = size in bytes
            'sizes': [],
            # str digits = last accessed time in seconds from epoch
            'acc_times': [],
            # str digits = last modified time in seconds from epoch
            'mod_times': [],
            # path like '/mnt/d' with depth=2
            'root_dir_paths': [],
            # path like '/maindir/subdir/lastdir/'
            'parent_dir_paths': [],
            # name of file from storage, end of path after '/', including extension
            'file_names': [],
            # found suffix at end of file_name, after '.'; can be extension like '.pdf'
            'suffixes': []
        }
        self.re_pattern = self._file_re_pattern()

    # def _file_re_pattern(self):
    #     # `stat -c "%F %s %X %Y %n" <file>` linux bash command
    #     file_type = r'regular file\s'
    #     size = acc_time = mod_time = r'(\d+)\s'
    #     # match path beginning with ./
    #     # parent_dir_path = r'(\.?\/.*\/)'
    #     parent_dir_path = r'\.?(\/.*\/)'
    #     # file_name returns [full_file_name, .ext or '']
    #     file_name = r'([^/]*?(\.\w+$|$))'

    #     return f'{file_type}{size}{acc_time}{mod_time}{parent_dir_path}{file_name}'

    def _file_re_pattern(self):
        # `stat -c "%F %s %X %Y %n" <file>` linux bash command
        file_type = r'regular file\s'
        size = acc_time = mod_time = r'(\d+)\s'
        # match path beginning with ./
        # parent_dir_path = r'(\.?\/.*\/)'
        parent_dir_path = r'\.?(\/.*\/)'
        # file_name returns [full_file_name, .ext or '']
        file_name = r'([^/]*?(\.\w+$|$))'

        return f'{file_type}{size}{acc_time}{mod_time}{parent_dir_path}{file_name}'

    def eat_file(self, file_path, limit=2):

        self.source_file_name = re.compile(r'.*\/([^/]*)$').match(file_path).group(1)
        file_stat_re = re.compile(self.re_pattern)

        with open(file_path) as file_reader:
            i = 1
            for line in file_reader:
                # limit for testing
                if i >= limit: break;

                if m := file_stat_re.match(line):
                    size, acc_time, mod_time, _,\
                    parent_dir_path, file_name, suffix = m.groups()

                    self.files_stat['i'].append(i)
                    self.files_stat['sizes'].append(size)
                    self.files_stat['acc_times'].append(acc_time)
                    self.files_stat['mod_times'].append(mod_time)
                    self.files_stat['parent_dir_paths'].append(parent_dir_path)
                    self.files_stat['file_names'].append(file_name)
                    self.files_stat['suffixes'].append(suffix)
                    i += 1
    
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