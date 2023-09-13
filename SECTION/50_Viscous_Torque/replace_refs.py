import os
import glob
import re

file_path = os.path.dirname(os.path.abspath(__file__))

with open(f'{file_path}{os.sep}replaces.txt', 'r') as in_file:
    subs = in_file.readlines()

search_folder = os.path.join(file_path, '20_Sections/')
names = glob.glob(search_folder+'*.tex')

for sub in subs:
    sub = sub.replace('\n', '')
    old, new = sub.split(',')
    for name in names:
        with open(name, "r") as myfile:
            data = myfile.readlines()
        with open(name, "wt") as myfile:
            for line in data:
                myfile.write(re.sub(old, new, line))
