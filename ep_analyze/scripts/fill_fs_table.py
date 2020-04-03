from ..models import FilesStat
from .file_stat import FS

# print(FS.files_stat.keys())

# fs = FilesStat()

def fill_fs_table(fs_dict):

    # number of records in arrays
    no_rec = len(fs_dict['id'])
    keys = fs_dict.keys()

    limit = 1
    for row in range(no_rec):
        # if row == limit: break;

        fs = FilesStat()

        fs.server_name = 'server'
        fs.server_addr = 'localhost' 
        fs.is_file = True 
        fs.size = int(fs_dict['sizes'][row])
        fs.acc_time = int(fs_dict['accesses'][row])
        fs.mod_time = int(fs_dict['modifications'][row])
        fs.root_dir_path = '/mnt/'
        fs.dir_path = fs_dict['directories'][row]
        fs.file_name = fs_dict['names'][row]
        fs.extension = fs_dict['suffixes'][row]
        
        fs.save()
    print('Done !')

def run():
    # fill_fs_table(FS.files_stat)
    pass

