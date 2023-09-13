import re
import os
import glob
root = os.path.dirname(os.path.abspath(__file__))
folder = '50_Viscous_Torque'
prefix = 'VT'

folder = '30_Timeconstant'
prefix = 'TC'


class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)

    def __enter__(self):
        return self.file_obj

    def __exit__(self, type, value, traceback):
        self.file_obj.close()


pattern = r'(sec|tab|eq|fig):(.+)(,|})'
#  pattern = r'(fig):(.+)}'


search_folder = os.path.join(root, folder, '20_Sections/')
names = glob.glob(search_folder+'*.tex')
for name in names:
    with open(name, "r") as myfile:
        data = myfile.readlines()
    with open(name, "wt") as myfile:
        for line in data:
            #  print(line)
            myfile.write(re.sub(pattern, r'\1:'+prefix+r'-\2}', line))
