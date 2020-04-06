import os, sys, re, io
from time import time
from django.apps import apps
from django.db import connection
from django.utils import timezone

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

    @property
    def _file_re_pattern(self):
        """
        Test online here https://regex101.com/ 
        """
        # `stat -c "%F %s %X %Y %n" <file>` linux bash command

        # match 'file' or 'directory'
        _type = r'(?:regular |)(?:empty |)(file|directory)\s'

        # match groups: (size) (acc_time) (mod_time) as digits
        size = acc_time = mod_time = r'(\d+)\s'

        # match path like /path/to/parent_dir/ 
        parent_dir_path = r'(\.?\/.*\/|)\/?'

        # name returns [full_file_name, .ext or ''] extension < 10 characters
        name = r'(\.?[^\/]*?(\.\w{1,9}$|$))'

        return f'{_type}{size}{acc_time}{mod_time}{parent_dir_path}{name}'
    
    # filestatbulk_to_table is too slow
    def __filestatbulk_to_table(self, file_stat_path, model):
        """
        Read source stat file, match patterns (fields) and insert to
        corresponding table (model) in database line by line
        """
        regex = re.compile(self._file_re_pattern)
        time_now = timezone.now().isoformat()

        lines_traveled = 0
        lines_matched = 0
        lines_not_matched = []

        # FileStat instances
        fs_instances = []
        t1 = time()
        with open(file_stat_path, 'r') as reader:

            for line in reader:
                lines_traveled += 1
                if m := regex.match(line):
                    lines_matched += 1
                    # if lines_matched >= 50000: break;

                    _type, size, acc_time, mod_time,\
                    parrent_dir_path, name, extension = m.groups()
                    
                    # convert _type from str to bool
                    _type == 'file' and (_type := True)
                    _type == 'directory' and (_type := False)

                    new_FileStat = model()

                    new_FileStat.server_name = 'DESKTOP-T77K7H1'
                    new_FileStat.server_addr = 'localhost'
                    new_FileStat.is_file = _type
                    new_FileStat.size = size
                    new_FileStat.acc_time = acc_time
                    new_FileStat.mod_time = mod_time
                    new_FileStat.parent_dir_path = parrent_dir_path
                    new_FileStat.name = name
                    new_FileStat.extension = extension
                    # new_FileStat.rec_timestamp = time_now
                    # new_FileStat.update_time = time_now
                    # new_FileStat.exists = True
                    # new_FileStat.exists_check_time = time_now

                    fs_instances.append(new_FileStat)

                else:
                    lines_not_matched.append(lines_traveled)

        model.objects.bulk_create(fs_instances)
        t2 = time()
        delta = t2 - t1
        print(f'{lines_traveled}/{lines_matched} lines matched')
        # print('lines not matched', lines_not_matched)
        sys.stderr.write(f'{sys._getframe(0).f_code.co_name} took {delta}')
    
    def filestream_to_table(self, file_stat_path, model):
        """
        Read provided file, match line, copy to in_memory StringIO(),
        then copy StringIO to table.
        """
        table_name = model._meta.db_table
        regex = re.compile(self._file_re_pattern)
        time_now = timezone.now().isoformat()
        in_memory_stream = io.StringIO()

        lines_traveled = 0
        lines_matched = 0
        lines_not_matched = []

        t1 = time()
        with open(file_stat_path, 'r') as reader:
            for line in reader:
                lines_traveled += 1

                m = regex.match(line)

                if m is None:
                    lines_not_matched.append(lines_traveled)
                    continue
                lines_matched += 1

                server_name = 'DESKTOP-9UTLJ6E'
                server_addr = 'localhost'

                _type, size, acc_time, mod_time,\
                parent_dir_path, name, extension = m.groups()

                _type == 'file' and (_type := 't')
                _type == 'directory' and (_type := 'f')
                
                rec_timestamp = time_now
                update_time = time_now
                exists = 't'
                exists_check_time = time_now

                
                line_to_write = '\t'.join(
                    (
                    server_name, server_addr,
                    _type, size, acc_time, mod_time,
                    parent_dir_path, name, extension,
                    rec_timestamp, update_time, exists, exists_check_time
                    )
                    )
                in_memory_stream.write(f'{line_to_write}\n')

        t2 = time()
        delta = t2 - t1
        sys.stdout.write(f'io.StringIO took:{delta:.2f} seconds\n')
        in_memory_stream.seek(0)

        with connection.cursor() as cursor:
            cursor.cursor.copy_from(
                file=in_memory_stream,
                table=table_name,
                sep='\t',
                columns=(
                'server_name', 'server_addr',
                'is_file', 'size', 'acc_time', 'mod_time',
                'parent_dir_path', 'name', 'extension',
                'rec_timestamp', 'update_time', 'exists', 'exists_check_time'
                )
            )
        in_memory_stream.close()
        t3 = time()

        delta = t3-t1
        print(f'{lines_traveled}/{lines_matched} lines matched')
        sys.stdout.write(f'{sys._getframe(0).f_code.co_name} took: {delta:.2f} seconds\n')
        # print('lines not matched', lines_not_matched)



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