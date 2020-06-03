from ..models import FileStat
import re

class Files:
    def __init__(self):
        self.files_dict = self.get_all_files()

    def get_all_files(self):
        files = FileStat.objects.values()
        return files
        
    def search(self, file_name):
        for file in self.files_dict:
            if file['extension'] == '.pdf':
                name = file['name']
                if re.search("%s" % file_name, name, flags=re.I):
                    print(name)
                    print(file['parent_dir_path'])
                    break
files = Files() 
print("count", len(files.files_dict))
files.search("goodrich")



def run():
    # print("hello from run")
    pass