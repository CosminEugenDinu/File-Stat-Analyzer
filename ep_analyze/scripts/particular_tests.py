from django.test import TestCase
import re
import sys


def test_FileStat_re_pattern(*args):
    # verbosity level
    v = True if 'v' in args else False
    if v1 := True if 'v1' in args else False:
        v = True
    if v2 := True if 'v2' in args else False:
        v1 = True; v = True

    from . import file_stat
    fs = file_stat.FileStat()

    compiled_pattern = re.compile(fs.re_pattern)

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
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'gram matik-aktiv-cornelsen.this_is_not_extension_because_is_grater_that_10', ''),
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

    # let's begin
    lines = dir_lines + file_lines

    def _messages():
        who_called_me = sys._getframe(1).f_code.co_name
        _success_msgs = ''
        _fail_msgs = ''
        _critical_msg = f'[{who_called_me}] finished with:\n'+\
            '----------------------------\n'
        
        def add_success_msg(msg):
            nonlocal _success_msgs
            _success_msgs += msg
            return True
        def add_fail_msg(msg):
            nonlocal _fail_msgs
            _fail_msgs += msg
            return True
        def add_critical(msg):
            nonlocal _critical_msg
            _critical_msg += msg
            return True
        def messages():
            nonlocal _success_msgs, _fail_msgs, _critical_msg
            return _success_msgs + _fail_msgs + _critical_msg

        return add_success_msg, add_fail_msg, add_critical, messages

    def test_match_line():
        suc, fail, crit, msg = _messages()

        not_matched = 0
        matched = 0
        total_lines = len(lines) // 2

        for i in range(0, len(lines), 2):
            src_str = lines[i]
            ref_matches = lines[i + 1]

            test_match = compiled_pattern.match(src_str)
            try:
                assert type(test_match) is not re.Match, 'no match'
            except AssertionError as e:
                not_matched += 1
                continue
            matched += 1
        
        v2 and suc(f'{matched}/{total_lines} lines matched\n')
        v1 and fail(f'{not_matched}/{total_lines} lines not matched\n')
        try:
            assert matched == total_lines, 'not all lines matched'
        except AssertionError as e:
            crit(str(e))
            return msg()

    print(test_match_line())
    


    # if d := compiled_pattern.match(line1):
    #     print(dir_m)
    # else:
    #     print('dir not matched', end='\n\n')
    
    # if file_m := compiled_pattern.match(line2):
    #     print(file_m)
    # else:
    #     print('file not matched')

    # for g in m.groups():
    #     print(repr(g))



def run(*args):
    """
    this function is called by django-extensions runscript
    """
    print('-------------------------')
    test_FileStat_re_pattern(*args)

def code_runner_direct_run():
    print('hello from code-runner')

# if __name__=='__main__':
#     code_runner_direct_run()

if __name__ == '__main__':
    unittest.main()