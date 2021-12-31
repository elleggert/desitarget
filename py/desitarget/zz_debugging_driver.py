import os
from cuts import select_targets
import pandas as pd

filenames = []

path = 'bricks_data/tractor'

for filename in os.listdir(path):
    if '.fits' not in filename:
        continue
    filenames.append(f'{path}/{filename}')


res = select_targets(
    infiles=filenames, numproc=1, qso_selection='colorcuts', nside=None, gaiasub=False,
    tcnames=['LRG', 'ELG', 'QSO'], backup=False)


