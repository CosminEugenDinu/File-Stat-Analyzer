from ..ep_files_stat.file_stat import FS
# print(*sorted(FS.suffixes().items(), key=lambda t:t[1], reverse=True), sep='\n')

def run():

    sizes = FS.pdf_sizes_ids()
    ss = sizes['same_sizes']
    us = sizes['unique_sizes']
    print('toate fisierele:', len(FS.files_stat['id']))
    print('toate pdf-urile:',len(FS.pdf_s_ids()))
    print('grupuri pdf-uri unice:', len(ss))
    print('pdf-uri unice:', len(us))


# def test():
#     sizes = FS.pdf_sizes_ids()
#     ss = sizes['same_sizes']
#     us = sizes['unique_sizes']

# if __name__=='__main__':
#     from timeit import Timer
#     t = Timer("test()", "from __main__ import test")
#     print('eat files took:', t.timeit(2))