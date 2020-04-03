import unittest
import re

def test_FileStat_re_pattern():
    from . import file_stat
    fs = file_stat.FileStat()
    pattern_comp = re.compile(fs.re_pattern)

    dir_lines = (
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/Gramatica''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', 'Gramatica', ''),
        # directory_name_ends_with.eprintare
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/Gramatica.eprintare''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', 'Gramatica.eprintare', ''),
        # directory_name_ends_with.eprintare.ro
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/Gramatica.eprintare.ro''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', 'Gramatica.eprintare.ro', ''),
        # .dirname 
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/.Gramatica''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', '.Gramatica', ''),
        # .dirname. 
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/.Gramatica.''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', 'Gramatica', ''),
        # root path begins with './' meaning that is not truly root 
        '''directory 512 1585856724 1528743541 ./mnt/comenzi/2018/06.Iunie/.08.06.2018/Bianca Constantin/.Gramatica.''',
        ('directory', '512', '1585856724', '1528743541', './mnt/comenzi', '/2018/06.Iunie/.08.06.2018/Bianca Constantin/', 'Gramatica', ''),

    )

    file_lines = (
        # .pdf
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsen.pdf', '.pdf'),
        # filenamepdf
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsenpdf''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsenpdf', ''),
        # filename.eprintare
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.eprintare''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsen.eprintare', '.eprintare'),
        # filename.
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsen.', ''),
        # .filename
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/.grammatik-aktiv-cornelsen''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsen.pdf', '.pdf'),
        # .filename.f
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsen.pdf', '.pdf'),
        # file name . no ext 
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/gram matik-aktiv-cornelsen . no ext''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'gram matik-aktiv-cornelsen . no ext', ''),
        # file name .no ext 
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/gram matik-aktiv-cornelsen .no ext''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'gram matik-aktiv-cornelsen .no ext', ''),
        # file name.this_is_not_extension_because_is_grater_that_10 
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/gram matik-aktiv-cornelsen.this_is_not_extension_because_is_grater_that_10''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'gram matik-aktiv-cornelsen.this_is_not_extension_because_is_grater_that_10, ''),
    )

    invalid_lines = (
        # invalit file type
        '''other file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        # invalid size
        '''regular file  _1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        # invalid access time mod time
        '''regular file 84522077 152__8743474 15282__73647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        '''regular file 84522077 15287434741528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        # invalid root_dir_path
        '''regular file 84522077 1528743474 1528273647 __/mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        # invalid trailing '/'
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf/''',
    )

    matches = (
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', 'Gramatica')
    matches2 = ('regular file', '84522077', '1528743474' '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsen.pdf')


    if dir_m := pattern_comp.match(line1):
        print(dir_m)
    else:
        print('dir not matched', end='\n\n')
    
    if file_m := pattern_comp.match(line2):
        print(file_m)
    else:
        print('file not matched')
    # for g in m.groups():
    #     print(repr(g))

def run():
    """
    this function is called by django-extensions runscript
    """
    print('-------------------------')
    test_FileStat_re_pattern()

def code_runner_direct_run():
    print('hello from code-runner')

if __name__=='__main__':
    code_runner_direct_run()
