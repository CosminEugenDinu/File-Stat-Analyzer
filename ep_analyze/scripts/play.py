import sys, re
import difflib
from time import time
from ..models import FileStat
from dev_tools.print_tools import dict_table_str 


def get_all_as_values(model):
    t = time()
    files = model.objects.values()
    delta = time() - t
    print('query objects:', len(files), f'({delta:.5f} sec)')
    return files

pdf_regex = re.compile('\.?pdf.*', re.I)
psd_regex = re.compile('\.?psd.*', re.I)

def get_count_extensions():
    files = get_all_as_values(FileStat)
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
    return {
        k: v
        for k, v in sorted(
            count_extensions.items(),
            key=lambda t: t[1],
            reverse=True
            )
        if v > 10 and k != ''
    }

# print(dict_table_str(get_count_extensions()))
# print(dict_table_str(get_count_extensions(), extended=True))


def get_pdf_extensions():
    count_extensions = get_count_extensions()
    pdf_extensions = {}
    t = time()
    for ext in count_extensions:
        if pdf_regex.match(ext):
            pdf_extensions[ext] = count_extensions[ext]
    d = time() - t
    print('pdf_extensions:', pdf_extensions, f'({d:.5f} sec)')


def get_by_ext(ext_pattern):
    files = get_all_as_values(FileStat)
    ext_regex = re.compile(ext_pattern, re.I)
    unique_sizes = {} 
    same_sizes = {} 
    t = time()
    for file in files:
        ext = file['extension']
        size = file['size']
        dir = file['parent_dir_path']
        name = file['name']
        if ext_regex.match(ext):
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
    return unique_sizes, same_sizes 

def analyze_same_sizes(ext_pattern):
    unique_sizes, same_sizes = get_by_ext(ext_pattern)
    # in same_sizes find the names that are the most similar
    # take the first array:
    longest_names_list = []
    longest_paths_list = []
    longest = (0, [], 0)
    same_sizes_lengths = {}
    len_54_info = None

    random = 555
    count = 0
    chosen_size = None
    for size in same_sizes:
        count += 1
        if count == random: chosen_size = size
        arr = same_sizes[size]
        if len(arr) > longest[0]:
            longest = (len(arr), arr, size)
        if same_sizes_lengths.get(len(arr)):
            same_sizes_lengths[len(arr)] += 1
        else:
            same_sizes_lengths[len(arr)] = 1
        if len(arr) == 54:
            len_54_info = same_sizes[size]

            
    for dir, name in longest[1]:
        longest_names_list.append(name)
        longest_paths_list.append(dir)

    # print(f'longest_names_list: {longest_names_list}')
    print(f'longest_names_list len, size: {longest[0]} {longest[2]}')
    # print(longest_paths_list[800])
    # print(same_sizes[chosen_size])
    print('same_sizes_lengths len', len(same_sizes_lengths))
    print('\nLEGEND')
    print(f'Descr: same sizes on {ext_pattern}')
    print('key: length of array with same sizes')
    print('idx:0: number of such array')
    print(dict_table_str(same_sizes_lengths, extended=True))
    # print(len_54_info)

            


def run():
    # sys.stdout.write('\nfrom run\n')
    analyze_same_sizes(r'.psd')
    analyze_same_sizes(r'.pdf')
    pass