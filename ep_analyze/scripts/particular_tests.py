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

    compiled_pattern = re.compile(fs._file_re_pattern())
    print(fs._file_re_pattern())
    dir_lines = (
        (
        # 0
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/Gramatica''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', 'Gramatica', ''),
        ),
        (
        # 1 directory_name_ends_with.eprintare; extension is .eprintare because I couldn't find a regex to exclude extension based on group 0 'directory'
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/Gramatica.eprintare''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', 'Gramatica.eprintare', '.eprintare'),
        ),
        (
        # 2 directory_name_ends_with.eprintare.ro
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/Gramatica.eprintare.ro''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', 'Gramatica.eprintare.ro', '.ro'),
        ),
        (
        # 3 .dirname 
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/.Gramatica''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', '.Gramatica', ''),
        ),
        (
        # 4 .dirname. 
        '''directory 512 1585856724 1528743541 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bianca Constantin/.Gramatica.''',
        ('directory', '512', '1585856724', '1528743541', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bianca Constantin/', '.Gramatica.', ''),
        ),
        (
        # 5 root path begins with './' meaning that is not truly root 
        '''directory 512 1585856724 1528743541 ./mnt/comenzi/2018/06.Iunie/.08.06.2018/Bianca Constantin/.Gramatica.''',
        ('directory', '512', '1585856724', '1528743541', './mnt/comenzi', '/2018/06.Iunie/.08.06.2018/Bianca Constantin/', '.Gramatica.', '')
        )
    )

    file_lines = (
        (
        # 6 .pdf
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsen.pdf', '.pdf'),
        ),
        (
        # 7 filenamepdf
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsenpdf''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsenpdf', ''),
        ),
        (
        # 8 filename.eprintare
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.eprintare''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsen.eprintare', '.eprintare'),
        ), 
        (
        # 9 filename.
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'grammatik-aktiv-cornelsen.', ''),
        ),
        (
        # 10 .filename
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/.grammatik-aktiv-cornelsen''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', '.grammatik-aktiv-cornelsen', ''),
        ),
        (
        # 11 .filename.f
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/.grammatik-aktiv-cornelsen.f''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', '.grammatik-aktiv-cornelsen.f', '.f'),
        ),
        (
        # 12 file name . no ext 
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/gram matik-aktiv-cornelsen . no ext''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'gram matik-aktiv-cornelsen . no ext', ''),
        ),
        (
        # 13 file name .no ext 
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/gram matik-aktiv-cornelsen .no ext''',
        ('regular file', '84522077', '1528743474', '1528273647', '/mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'gram matik-aktiv-cornelsen .no ext', ''),
        ),
        (
        # 14 file name.this_is_not_extension_because_is_grater_that_10 
        '''regular file 84522077 1528743474 1528273647 ./mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/gram matik-aktiv-cornelsen.this_is_not_extension_because_is_grater_that_10''',
        ('regular file', '84522077', '1528743474', '1528273647', './mnt/comenzi', '/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/', 'gram matik-aktiv-cornelsen.this_is_not_extension_because_is_grater_that_10', '')
        )
    )

    invalid_lines = (
        # 0 invalid file type
        '''other file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        # 1 invalid size
        '''regular file  _1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        # 2 invalid access time mod time
        '''regular file 84522077 152__8743474 15282__73647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        # 3 
        '''regular file 84522077 15287434741528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        # 4 invalid root_dir_path
        '''regular file 84522077 1528743474 1528273647 __/mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf''',
        # 5 invalid trailing '/'
        '''regular file 84522077 1528743474 1528273647 /mnt/comenzi/2018/06.Iunie/08.06.2018/Bia. C. C-tin/Gramatica/grammatik-aktiv-cornelsen.pdf/''',
    )

    # let's begin
    lines = dir_lines + file_lines
    
    def Messages(comment=''):
        """
        Returns tuple of 2 closures.

        Ussage example:

        add_info_msg, get_info_msgs = Messages('Info')
        add_success_msg, get_success_msgs = Messages('Success')
        add_failure_msg, get_failures_msgs = Messages('Fail')

        for i in range(10):
            add_success_msg('line matched')
        
        add_success_msg('Method succeeded')

        str_for_print = ''.join(f'{value} {msg}\n' 
            for msg, value in get_success_msgs().items())

        print(str_for_print)
        """

        _who_called_me = sys._getframe(1).f_code.co_name
        _msgs_count = {_who_called_me: comment}
        
        def add_msg(msg):
            nonlocal _msgs_count

            if type(msg) is not str:
                raise Exception('msg must be of type str')

            if _msgs_count.get(msg) is not None:
                _msgs_count[msg] += 1
            else:
                _msgs_count[msg] = 1

            return True
        
        def get_msgs():
            nonlocal _msgs_count
            return _msgs_count

        return add_msg, get_msgs

    def str_messages(*dict_messages):

        def human_str(msg_dict):
            return ''.join(f'{value} {msg}\n' for msg, value in msg_dict.items())
        def records_str(msg_dict):
            return f'total records {len(msg_dict) -1}\n'
        def dashed_line(dashes):
            return '-' * dashes + '\n'
            
        str_for_print = ''
        dashes = 20
        for msg_dict in dict_messages:
            str_for_print += human_str(msg_dict)
            str_for_print += records_str(msg_dict)
            str_for_print += dashed_line(dashes)
        
        return str_for_print

    def test_match_line(lines):

        add_info_msg, get_info_msgs = Messages('Info')
        add_success_msg, get_success_msgs = Messages('Success')
        add_failure_msg, get_failures_msgs = Messages('Fail')

        for i in range(len(lines)):

            add_info_msg('traveled cases')
            src_str = lines[i][0]
            ref_match_groups = lines[i][1]

            test_match = compiled_pattern.match(src_str)
            try:
                assert type(test_match) is re.Match, \
                    'line not matched at all'
            except AssertionError as e:
                add_failure_msg(str(e))
                continue
            add_success_msg('line matched')
            
            match_groups = test_match.groups()
            try:
                assert len(match_groups) == len(ref_match_groups)
            except AssertionError as e:
                add_failure_msg('wrong length of match_groups')
                continue
            add_success_msg('correct length of match_groups')

            # compare each match group with coresponding reference
            for j in range(len(ref_match_groups)):
                try:
                    assert match_groups[j] == ref_match_groups[j], \
                        f'group {j} did not matched at case {i}'
                except AssertionError as e:
                    add_failure_msg(str(e))
                    print('wrong', match_groups[j])
                    continue
                add_success_msg(
                    f'group {j} matched at case {i}'
                )

        messages = []
        # verbosity level
        v1 and messages.append(get_info_msgs())
        v2 and messages.append(get_success_msgs())
        v and messages.append(get_failures_msgs())
        
        return messages

    def test_not_match_line(invalid_lines):

        add_info_msg, get_info_msgs = Messages('Info')
        add_success_msg, get_success_msgs = Messages('Success')
        add_failure_msg, get_failures_msgs = Messages('Fail')

        for i in range(len(invalid_lines)):

            add_info_msg('traveled cases')
            invalid_src_str = invalid_lines[i]

            test_match = compiled_pattern.match(invalid_src_str)
            try:
                assert test_match is None, \
                    f'incorrectly matched invalid_lines[{i}]'
            except AssertionError as e:
                add_failure_msg(str(e))
                continue
            add_success_msg('correctly not matched invalid_lines')



        messages = []
        # verbosity level
        v1 and messages.append(get_info_msgs())
        v2 and messages.append(get_success_msgs())
        v and messages.append(get_failures_msgs())

        return messages

    match_line_msgs = test_match_line(lines)
    not_match_line_msgs = test_not_match_line(invalid_lines)
    messages = match_line_msgs + not_match_line_msgs

    print(str_messages(*match_line_msgs))
    print(str_messages(*not_match_line_msgs))

    return messages
    


def run(*args):
    """
    this function is called by django-extensions runscript
    """
    print('-------------------------')
    messages = test_FileStat_re_pattern(*args)
    print(messages)

def code_runner_direct_run():
    print('hello from code-runner')

# if __name__=='__main__':
#     code_runner_direct_run()

if __name__ == '__main__':
    unittest.main()