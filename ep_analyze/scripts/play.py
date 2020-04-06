import sys, re
import difflib
from time import time
from ..models import FileStat

t = time()
files = FileStat.objects.values()
delta = time() - t
print('query objects:', len(files), f'({delta:.5f} sec)')
pdf_regex = re.compile('\.?pdf.*', re.I)


count_extensions = {}
t = time()
for file in files:
    ext = file['extension']
    if count_extensions.get(ext):
        count_extensions[ext] += 1
    else:
        count_extensions[ext] = 1
delta = time() -t
print('distinct extensions:',
    len(count_extensions), f'({delta:.5f} sec)')


pdf_extensions = {}
t = time()
for ext in count_extensions:
    if pdf_regex.match(ext):
        pdf_extensions[ext] = count_extensions[ext]
d = time() - t
print('pdf_extensions:', pdf_extensions, f'({d:.5f} sec)')


pdf_s = { 'unique_sizes': {}, 'same_sizes': {} }
unique_sizes = pdf_s['unique_sizes']
same_sizes = pdf_s['same_sizes']
t = time()
for file in files:
    ext = file['extension']
    size = file['size']
    dir = file['parent_dir_path']
    name = file['name']
    if pdf_regex.match(ext):
        if s := same_sizes.get(size):
            s.append((dir, name))
        elif array := unique_sizes.get(size):
            array.append((dir, name))
            same_sizes[size] = array
            del unique_sizes[size]
        else:
            unique_sizes[size] = [(dir, name)]
d = time() -t
print(f'pdf_s = \
{{unique_sizes: {len(unique_sizes)}, \
same_sizes: {len(same_sizes)}}}', f'({d:.5f} sec)')

# in same_sizes find the names that are the most similar
# take the first array:
longest_names_list = []
longest_paths_list = []
longest = (0, [], 0)
for size in same_sizes:
    arr = same_sizes[size]
    if len(arr) > longest[0]:
        longest = (len(arr), arr, size)
        
for dir, name in longest[1]:
    longest_names_list.append(name)
    longest_paths_list.append(dir)

# print(f'longest_names_list: {longest_names_list}')
print(f'longest_names_list len, size: {longest[0]} {longest[2]}')
print(longest_paths_list[800])



            


def run():
    # sys.stdout.write('\nfrom run\n')
    pass