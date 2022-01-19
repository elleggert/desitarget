import os
from cuts import select_targets, format_output

filenames = []

path = 'bricks_data/tractor'
path = '/Volumes/Astrostick/bricks_data/south/'


for filename in os.listdir(path):
    if '.fits' not in filename:
        continue
    filenames.append(f'{path}/{filename}')

res = select_targets(
    infiles=filenames, numproc=1, qso_selection='colorcuts', nside=None, gaiasub=False,
    tcnames=["LRG","ELG","QSO", 'LBG'], backup=False)


# TODO:
#  1. DROP UNNECESSARY ITEMS
#  2. COMPUTE SNRS
#  3. FIX TARGETMASK --> EITHER FORK DESIUTIL OR SIMPLY ALTER TARGETMASK.YAML

df = format_output(result=res)

print((df.head()))
print(f"No of LRG       : {len(df[df['LRG'] == True])}")
print(f"No of ELG       : {len(df[df['ELG'] == True])}")
print(f"No of QSO       : {len(df[df['QSO'] == True])}")
print(f"No of G Dropouts: {len(df[df['GLBG'] == True])}")
print(f"No of R Dropouts: {len(df[df['RLBG'] == True])}")

