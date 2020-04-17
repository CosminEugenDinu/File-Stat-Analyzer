import sys, re, csv
from time import time
from collections import defaultdict, Counter

from ..models import FileStat as FileStatModel
from ..models import FilesRelatives as FilesRelativesModel

from dev_tools.print_tools import dict_table_str


class AnalyzeFiles:

    class Analyze:
        def __init__(self, _dict):
            self.data = _dict
            self.legend = {}
            self.extended_print = True
            self.print_options = {}

        def __str__(self):
            str_for_print = '\nLEGEND:\n'
            str_for_print += dict_table_str(
                self.legend, separators=False,
                extended=self.extended_print
            )
            str_for_print += dict_table_str(self.data,
                **self.print_options
            )
            return str_for_print


    def __init__(self):
        self.FileStatModel = FileStatModel
        # self.files = self.get_all_files_db()

    def get_all_files_db(self):
        t = time()
        files = self.FileStatModel.objects.values()
        delta = time() - t
        print('query objects:', len(files), f'({delta:.5f} sec)')
        return files
    
    def all_extensions(self):
        files = self.get_all_files_db() 
        count_extensions = defaultdict(int)
        t = time()
        for file in files:
            if not file['is_file']:
                continue
            ext = file['extension']
            count_extensions[ext] += 1
        delta = time() - t


        sorted_extensions = {
            k: v
            for k, v in sorted(
                count_extensions.items(),
                key=lambda t: t[1],
                reverse=True
                )
            if v > 2 and k != ''
        }
        legend = {
        'Descr:': 'All extensions.',
        'Total:': f"{len(count_extensions)} distinct extensions ({delta:.5f} sec)",
        'key:': 'extension of file',
        'idx:0:': 'number of files with that extension',
        }
        A = self.Analyze(sorted_extensions)
        A.legend = legend
        A.print_options = dict(indexes=True)
        return A

    def relatives(self, extension_regex):
        """
        Get all files with provided extension that are related by size
        and by name.
        """
        model = FilesRelativesModel
        ext_re = re.compile(extension_regex)
        files = self.get_all_files_db()

        # for file in files:
    
    def file_list(self, **filters):

        class FileList(self.Analyze):

            def save(self, path):
                with open(path, 'w') as csvfile:
                    csv_w = csv.writer(csvfile, delimiter='\t')
                    data = self.data
                    for i in range(len(data['id'])):
                        id = data['id'][i]
                        size = data['size'][i]
                        path = data['path'][i]
                        csv_w.writerow((id, size, path))
        
        """
        Return list of tuples (id, path).
        Some sizes are ignored (like 4096).
        When sizes are identical, get only one occurrence, based on
        some criteria.
        Filters: ext, size
        """

        if (_ext := filters.get('ext')):
            ext_re = re.compile(f"^\.?{_ext}", re.I)
        else:
            ext_re = re.compile('.*')
        
        if (_root_dir := filters.get('root_dir')):
            root_dir_re = re.compile(f"^({_root_dir}).*")
        else:
            root_dir_re = re.compile('.*')


        files = self.get_all_files_db()

        sizes_count = defaultdict(int)
        
        file_list = defaultdict(list) 

        for file in files:
            size = file['size']
            dir = file['parent_dir_path']
            fn = file['name']
            ext = file['extension']

            # filters
            if not file['is_file']: continue
            if not ext_re.match(ext): continue
            if not root_dir_re.match(dir): continue
            if size < 8000: continue
            
            sizes_count[size] += 1

            if sizes_count.get(size) > 1:
                pass
            else:
                file_list['id'].append(file['id'])
                file_list['size'].append(size)
                file_list['path'].append(dir+fn)
        
        # switch keys with values 
        count_sizes = {
            v: k
            for k, v in sizes_count.items()
            if v > 1
        }

        num_of_copies_str = '\n'+ \
            f"num of copies with ext: {_ext}\n" + \
            dict_table_str({
            "count": 'size',
            '-----': '-----',
            **count_sizes
            }, col_len=12, separators=False)

        # print(num_of_copies_str)
    
        # print(dict_table_str(
        #     file_list, extended=False, col_len=40))
        
        # print(file_list['path'][0])

        FL = FileList(file_list)
        FL.print_options = dict(
            extended=False,
            col_len=20
        ) 
        return FL

        



AF = AnalyzeFiles()

# print(AF.all_extensions())

# print(AR.relatives(r'\.?pdf.*')))

filelist = AF.file_list(ext='pdf',
    root_dir='/mnt/comenzi|/mnt/drive|/mnt/privat',
    min_size=8000)
# print(filelist)
# filelist.save('filelist.csv')

with open('filelist.csv', 'r', newline='') as csvfile:
    csv_r = csv.reader(csvfile, delimiter='\t')
    count = 0
    for row in csv_r:
        count += 1
        if count > 20: break
        print(row)

def run():
    pass

# some_dict = {
#     'em_str': '',
#     'some_str': 'string',
#     'arr': [1, 2, 3],
#     'nes_dic': {'s_key1':1, 7:'seven'},
#     'bo': True,
#     'no': None,
#     'int': 10
# }

# print(dict_table_str(some_dict))
# print(dict_table_str(some_dict, indexes=True))
# print(dict_table_str(some_dict, separators=False, indexes=True))
# print(dict_table_str(some_dict, extended=False))
# print(dict_table_str(some_dict, extended=False, indexes=True))
# print(dict_table_str(
#     some_dict, extended=False, indexes=True, separators=False))