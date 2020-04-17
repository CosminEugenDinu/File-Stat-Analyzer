import re
import sys


def dict_table_str(
    _dict, extended=True, col_len=7, 
    indexes=False, separators=False, limit=20,
):

    if type(_dict).__name__ not in ['dict', 'defaultdict', 'Counter']:
        raise TypeError('only type dict, defaultdict, Counter accepted')
    if len(_dict) > 1000:
        raise Exception('more than 1000 keys')

    if not separators:
        indexes = False
    v_sep = '|' if separators else ''


    if col_len < 7:
        col_len = 7

    def keys_values():
        """
        extended=True
        """
        str_for_print = ''
        line_interval = f"{'-'*col_len}"
        columns = 1
        start_idx_count = 0
        rows = []

        for k in _dict:
            key_str = f"{k}{' '*(col_len - len(str(k)))}{v_sep}" if len(str(k)
                                                                  ) <= col_len else f"{str(k)[0:col_len]}{v_sep}"
            if (val:= _dict.get(k)) is None:
                key_str += f"{val}{' '*(col_len-len(f'{val}'))} "
            elif type(val) is str:
                if len(val) == 0:
                    key_str += repr(val)
                    rows.append(key_str+'\n')
                    continue
                else:
                    key_str += val
                    rows.append(key_str+'\n')
                    continue
            elif val is False or val is True or type(val) is int:
                key_str += repr(val)
                rows.append(key_str+'\n')
                continue
            else:
                if len(val) > columns:
                    columns = len(val)
                for elem in val:
                    elem_str = str(elem)
                    key_str += f"{elem_str}{' '*(col_len-len(elem_str))} " if len(
                        elem_str) <= col_len else f"{elem_str[0:col_len]} "
            rows.append(key_str + '\n')

        border_top = f"{'_'*col_len}_{(('_'*col_len)+'_')*columns}\n"
        complete_line = f"{line_interval}{v_sep}"*columns+line_interval+'-'+'\n'
        complete_line_only_dashes = f"{line_interval}{v_sep}{(line_interval+'-')*columns}"+'\n'

        idx_str = [f'{i}' for i in range(
            start_idx_count, columns+start_idx_count)]
        fix_len_idx_str = []

        for idx in idx_str:
            fix_len_idx_str.append(
                f"{idx}{' '*(col_len-len(idx))}" if len(idx) <= col_len else f"{idx[0:col_len]}")

        top_left = f"key\\idx{' '*(col_len-7)}{v_sep}"
        header = top_left+f'{v_sep}'.join(fix_len_idx_str)+'\n'
        str_for_print += border_top

        if indexes:
            str_for_print += header
            str_for_print += complete_line
        if separators:
            str_for_print += f"{complete_line_only_dashes}".join(rows)
        else:
            str_for_print += ''.join(rows)

        str_for_print = re.sub(r'\n', f'\n{v_sep}', str_for_print)
        return str_for_print

# '.................................................................................'
    def values_keys():
        str_for_print = ''
        # compensate some spaces
        s = ' ' if separators else ''
        line_interval = f"{'-'*col_len}"
        empty_fix_len_str = ' '*col_len
        iter_idx = 0
        rows = []
        keys_str = [f'{k}' for k in _dict.keys()]

        columns = len(keys_str)
        # where _dict[some_key] has a dict as value, store those nested dict keys as a list
        nested_dict_keys_lists = {}

        end = False
        while not end:
            end = True

            row = ''
            for key in _dict:

                val = _dict.get(key)
                val_type = type(val)
                val_str = ''

                if iter_idx == 0:
                    if (val is None) or (val_type is bool) or (val == ''):
                        val_str = repr(val)
                    elif val_type is int:
                        val_str = str(val)
                    elif val_type is str:
                        val_str = val

                if type(val) is dict:
                    if (nested_keys:= nested_dict_keys_lists.get(key)) is None:
                        nested_dict_keys_lists[key] = list(_dict[key].keys())
                        nested_keys = nested_dict_keys_lists.get(key)
                    try:
                        val_str = repr(nested_keys[iter_idx])
                        end = False
                    except IndexError:
                        val_str = empty_fix_len_str
                elif (type(val) is list) or (type(val) is tuple):
                    try:
                        val_str = repr(val[iter_idx])
                        end = False
                    except IndexError:
                        val_str = empty_fix_len_str

                row += f"{val_str[0:col_len]}{s}" if len(
                    val_str) > col_len else f"{val_str}{s}{' '*(col_len-len(val_str))}"

            if indexes:
                idx_str = str(iter_idx)
                fix_len_idx_str = f"{idx_str}{' '*(col_len-len(idx_str))}{v_sep}"
            else:
                fix_len_idx_str = ''

            if not end:
                rows.append(f"{v_sep}{fix_len_idx_str}{row}")

            iter_idx += 1

        fix_len_keys_str = []
        for key_str in keys_str:
            fix_len_keys_str.append(f"{key_str[0:col_len]}" if len(
                key_str) > col_len else f"{key_str}{' '*(col_len-len(key_str))}")

        if indexes:
            border_top = f"{'_'*col_len}_{(('_'*col_len)+'_')*columns}\n"
            top_left = f"{v_sep}idx\\key{' '*(col_len-7)}{v_sep}" 
            complete_line_only_dashes = f"\n{v_sep}{line_interval}{v_sep}{(line_interval+'-')*columns}"+'\n'
            complete_line = f"{line_interval}{v_sep}"*columns+line_interval+'-'+'\n'
        else:
            border_top = f"{'_'*col_len*(columns+1)}\n"
            top_left = f'{v_sep}'
            complete_line_only_dashes = f"\n{v_sep}{line_interval*(columns+1)}\n"
            complete_line = f"{line_interval}"*(columns+1)+'\n'

        header = top_left+f"{v_sep}".join(fix_len_keys_str)+'\n'

        str_for_print += border_top
        str_for_print += header
        if separators:
            str_for_print += f"{v_sep}{complete_line}"
            str_for_print += f"{complete_line_only_dashes}".join(rows)
        else:
            str_for_print += '\n'.join(rows)
        # str_for_print += '\n'.join(rows)

        return str_for_print

    return keys_values() if extended else values_keys()
