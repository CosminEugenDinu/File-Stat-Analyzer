import os
import re
from time import time
from django.apps import apps

# linux command:
# $ find . -exec stat -c "%F %s %X %Y %n" {} \; > file
# %F=fileType %s=totalSizeBytes %X=lastAccess %Y=lastModification %n=fileName


class FileStat:

    def __init__(self):
        self.files_stat = {
            'id': [],
            'stat_file_names': [],
            'sizes': [],
            'births': [],
            'accesses': [],
            'modifications': [],
            'directories': [],
            'names': [],
            'suffixes': []
        }
        self.re_pattern = ''

    def eat_file(self, file_path):

        stat_file_name = re.compile(r'.*\/([^/]*)$').match(file_path).group(1)
        file_stat_re = re.compile(self.re_pattern)

        with open(file_path) as file_reader:
            id = 1
            for line in file_reader:
                if m := file_stat_re.match(line):
                    size, birth, access, modification, _,\
                    directory, name, suffix = m.groups()

                    self.files_stat['id'].append(id)
                    self.files_stat['stat_file_names'].append(stat_file_name)
                    self.files_stat['sizes'].append(size)
                    self.files_stat['births'].append(birth)
                    self.files_stat['accesses'].append(access)
                    self.files_stat['modifications'].append(modification)
                    self.files_stat['directories'].append(directory)
                    self.files_stat['names'].append(name)
                    self.files_stat['suffixes'].append(suffix)
                    id += 1
    
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
        id_int from self.files_stat['id']
        """
        sizes = {
            'same_sizes': {},
            'unique_sizes': {}
        }

        pdf_s_ids = self.pdf_s_ids()

        for id in pdf_s_ids:
            # if id > 10000: break;

            name = self.files_stat['names'][id]
            size = self.files_stat['sizes'][id]

            if ss := sizes['same_sizes'].get(size):
                ss.append(id)
            elif us_id := sizes['unique_sizes'].get(size):
                sizes['same_sizes'][size] = [us_id, id]
                del sizes['unique_sizes'][size]
            else:
                sizes['unique_sizes'][size] = id

        return sizes
    
    def pdf_same_sizes_names(self):
        """
        Iterates through lists of same size pdf_s and get only the first occurrence as name.
        Returns list of pdf_s names.
        """
        pdf_names = []



        return pdf_names

    def pdf_unique_sizes_names(self):
        """
        Return list of pdf file_names with unique sizes.
        """
        pdf_names = []

        return pdf_names



def file_re_pattern():
    file_type = r'regular file\s'
    # sWXYZ "%s %W %X %Y %Z" in stat linux bash command
    size = birth = access = modification = change = r'(\d+)\s'
    dir_path = r'(\.?\/.*\/)'
    # file_name returns [full_file_name, .ext or '']
    file_name = r'([^/]*?(\.\w+$|$))'

    return file_type + size + birth + access + modification + change + \
        dir_path + file_name

# line = "regular file 84908320 0 1535538397 1517314540 1517314540 ./1.Comenzi Clienti/2018/02. Februarie/01.02.2018/Aldea Stefan/" +\
# "345506492-Curs-de-Chirurgie-Pentru-Studenti-Anii-IV-Si-v-M-Beuran-Vol-I-2013" + \
# ".pdf"
# m = file_stat_re.match(line)
# for g in m.groups():
#     print(repr(g))


app_path = apps.get_app_config('ep_analyze').path
files_stat_path = os.path.join(app_path, 'ep_files_stat')

drive_stat_path = os.path.join(files_stat_path, 'drive_stat_FsWXYZn')
comenzi_1_stat_path = os.path.join(files_stat_path, 'comenzi_2015_stat_FsWXYZn')
comenzi_2_stat_path = os.path.join(files_stat_path, 'comenzi_2016_2018_stat_FsWXYZn')
comenzi_3_stat_path = os.path.join(files_stat_path, 'comenzi_stat_FsWXYZn_')

FS = FileStat()
FS.re_pattern = file_re_pattern()
# print('eat files begin:', t1:=time())
FS.eat_file(drive_stat_path)
FS.eat_file(comenzi_1_stat_path)
FS.eat_file(comenzi_2_stat_path)
FS.eat_file(comenzi_3_stat_path)
# print('eat files end', t2:=time())
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