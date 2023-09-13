import os
import re
import numpy as np
from jellyfish import jaro_distance

file_path = os.path.dirname(os.path.abspath(__file__))
print(file_path)


class Bib:

    def __init__(self, name: str) -> None:

        self.name = name
        self.entries = {}

    def read_file(self) -> None:
        with open(self.name, 'r') as myfile:
            self.data = myfile.readlines()

    def find_entries(self) -> None:
        pattern_key = r'@\w+{(.+),$'
        pattern_title = r'title ?= ?{(.+)},$'

        need_key = True
        title = None

        for line in self.data:
            if need_key and re.findall(pattern_key, line):
                key = re.findall(pattern_key, line)[0]
                need_key = False
            if not need_key and re.findall(pattern_title, line):
                title = re.findall(pattern_title, line)[0].lower()
                need_key = True

            if title is not None:
                self.entries[key] = title
                title = None
                key = None

    def get_title(self, key: str) -> str:
        return self.entries[key]

    @property
    def L(self) -> int:
        return len(self)


bib_old = Bib(os.path.join(file_path, 'alle_referenzen.bib'))
bib_old.read_file()
bib_old.find_entries()

bib_new = Bib(os.path.join(file_path, '../../All.bib'))
bib_new.read_file()
bib_new.find_entries()

matches = {}
unmatched = {}
for key, value in bib_old.entries.items():
    o_title = value
    scores = []
    for n_key, n_value in bib_new.entries.items():
        scores.append(jaro_distance(value, n_value))
    max_score = max(scores)
    if max_score > 0.9:

        print(f'searching for {key} with title:\n\t{value}')
        index = scores.index(max_score)
        best_key = list(bib_new.entries.keys())
        best_key = best_key[index]
        best_title = bib_new.get_title(best_key)
        print(f'best match: {best_key} --> {max_score:.3f}\n\t{best_title}\n')

        matches[key] = best_key
    else:
        unmatched[key] = value

with open(f'{file_path}/out.txt', 'w') as out:
    for key, value in matches.items():
        out.write(f'{key},{value}\n')


for key, value in unmatched.items():
    print(key, value, end='\n\n')
