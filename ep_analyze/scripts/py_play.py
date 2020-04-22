from collections import defaultdict
from dev_tools.print_tools import dict_table_str

d = defaultdict(int)

d['key1'] += 1
d['key2'] += 1
d['key3'] += 1
d['key3'] += 1

print(dict_table_str(d))

