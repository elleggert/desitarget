import os
import pandas as pd
from cuts import select_targets, format_output
import healpy as hp
import numpy as np

# Defining important metrics and functions

# Setting NSIDE values
NSIDE = 256
NPIX = hp.nside2npix(NSIDE)


# Todo: check desitarget api if there is a equivalent function inside desitarget
def raDec2thetaPhi(ra, dec):
    return (0.5 * np.pi - np.deg2rad(dec)), (np.deg2rad(ra))


# Set path to where all northern bricks are
path = '/Volumes/Astrostick/bricks_data/south/'
area = 'north'
bricks_block_size = 5000

# If working from file directory
filenames = [f'{path}/{filename}' for filename in os.listdir(path) if '.fits' in filename]

# Generate Empty DF to append to on disk
df = pd.DataFrame(columns=['RA', 'DEC', 'DCHISQ', 'FLUX_G', 'FLUX_R', 'FLUX_Z', 'FLUX_W1',
                           'FLUX_W2', 'LRG', 'ELG', 'QSO', 'GLBG', 'RLBG', 'GSNR', 'RSNR', 'ZSNR', 'W1SNR', 'W2SNR'])

path = '/Users/edgareggert/astrostatistics/bricks_data/tractor'

df.to_csv(f'{path}/redshift_catalogue_{area}.csv', mode='w', index=False, header=True)

for i in range(0, len(filenames), bricks_block_size):
    filenames_subset = filenames[i:i + bricks_block_size]
    if not filenames_subset:
        continue
    print(i, i + bricks_block_size, len(filenames_subset))
    # Alter numproc parameter here
    res = select_targets(
        infiles=filenames_subset, numproc=1, qso_selection='colorcuts', nside=256, gaiasub=False,
        tcnames=["LRG", "ELG", "QSO", 'LBG'], backup=False)

    df = format_output(result=res)

    # Exporting the Galaxy Catalogue by appending to existing extraction:
    df.to_csv(f'{path}/redshift_catalogue_{area}.csv', mode='a', index=False, header=False)

# Computing some summary statistics

df = pd.read_csv(f'{path}/redshift_catalogue_{area}.csv', dtype={'RA': 'float64',
                                                                 'DEC': 'float64',
                                                                 'DCHISQ': 'object',
                                                                 'FLUX_G': 'float64',
                                                                 'FLUX_R': 'float64',
                                                                 'FLUX_Z': 'float64',
                                                                 'FLUX_W1': 'float64',
                                                                 'FLUX_W2': 'float64',
                                                                 'LRG': 'bool',
                                                                 'ELG': 'bool',
                                                                 'QSO': 'bool',
                                                                 'GLBG': 'bool',
                                                                 'RLBG': 'bool',
                                                                 'GSNR': 'float64',
                                                                 'RSNR': 'float64',
                                                                 'ZSNR': 'float64',
                                                                 'W1SNR': 'float64',
                                                                 'W2SNR': 'float64'})

print(NPIX)

print(f"Total Objects   : {len(df)}")
print(f"No of LRG       : {len(df[df['LRG'] == True])}")
print(f"No of ELG       : {len(df[df['ELG'] == True])}")
print(f"No of QSO       : {len(df[df['QSO'] == True])}")
print(f"No of G Dropouts: {len(df[df['GLBG'] == True])}")
print(f"No of R Dropouts: {len(df[df['RLBG'] == True])}")

# LRG
df_LRG = df[df["LRG"] == True]
ra_LRG = df_LRG["RA"].to_numpy(copy=True)
dec_LRG = df_LRG["DEC"].to_numpy(copy=True)
theta, phi = raDec2thetaPhi(ra_LRG, dec_LRG)
LRG_pixel_indices = hp.ang2pix(NSIDE, theta, phi)
# Finding out unique indices and how often they appear --> shows the density of LRGs in this pixel
(unique, counts) = np.unique(LRG_pixel_indices, return_counts=True)
print(f"Mean LRGs per 256-Pixel: {counts.mean()}")

# ELG
df_ELG = df[df["ELG"] == True]
ra_ELG = df_ELG["RA"].to_numpy(copy=True)
dec_ELG = df_ELG["DEC"].to_numpy(copy=True)
theta, phi = raDec2thetaPhi(ra_ELG, dec_ELG)
ELG_pixel_indices = hp.ang2pix(NSIDE, theta, phi)
# Finding out unique indices and how often they appear --> shows the density of LRGs in this pixel
(unique, counts) = np.unique(ELG_pixel_indices, return_counts=True)
print(f"Mean ELGs per 256-Pixel: {counts.mean()}")

# QSO
df_QSO = df[df["QSO"] == True]
ra_QSO = df_QSO["RA"].to_numpy(copy=True)
dec_QSO = df_QSO["DEC"].to_numpy(copy=True)
theta, phi = raDec2thetaPhi(ra_QSO, dec_QSO)
QSO_pixel_indices = hp.ang2pix(NSIDE, theta, phi)
# Finding out unique indices and how often they appear --> shows the density of LRGs in this pixel
(unique, counts) = np.unique(QSO_pixel_indices, return_counts=True)
print(f"Mean QSOs per 256-Pixel: {counts.mean()}")

# GLBG
df_GLBG = df[df["GLBG"] == True]
ra_GLBG = df_GLBG["RA"].to_numpy(copy=True)
dec_GLBG = df_GLBG["DEC"].to_numpy(copy=True)
theta, phi = raDec2thetaPhi(ra_GLBG, dec_GLBG)
GLBG_pixel_indices = hp.ang2pix(NSIDE, theta, phi)
# Finding out unique indices and how often they appear --> shows the density of LRGs in this pixel
(unique, counts) = np.unique(GLBG_pixel_indices, return_counts=True)
print(f"Mean GLBGs per 256-Pixel: {counts.mean()}")

# RLBG
df_RLBG = df[df["RLBG"] == True]
ra_RLBG = df_RLBG["RA"].to_numpy(copy=True)
dec_RLBG = df_RLBG["DEC"].to_numpy(copy=True)
theta, phi = raDec2thetaPhi(ra_RLBG, dec_RLBG)
RLBG_pixel_indices = hp.ang2pix(NSIDE, theta, phi)
# Finding out unique indices and how often they appear --> shows the density of LRGs in this pixel
(unique, counts) = np.unique(RLBG_pixel_indices, return_counts=True)
print(f"Mean RLBGs per 256-Pixel: {counts.mean()}")

# All Objects
ra = df["RA"].to_numpy(copy=True)
dec = df["DEC"].to_numpy(copy=True)
theta, phi = raDec2thetaPhi(ra, dec)
pixel_indices = hp.ang2pix(NSIDE, theta, phi)
# Finding out unique indices and how often they appear --> shows the density of LRGs in this pixel
(unique, counts) = np.unique(pixel_indices, return_counts=True)
print(f"Mean Objects per 256-Pixel: {counts.mean()}")
print(f"Total pixels touched by sample bricks: {len(unique)}")

# Dropping columns not needed for galaxy density computation
df.drop(inplace=True, axis=1, columns=['DCHISQ', 'FLUX_G', 'FLUX_R', 'FLUX_Z', 'FLUX_W1',
                                       'FLUX_W2', 'GSNR', 'RSNR', 'ZSNR', 'W1SNR', 'W2SNR'])
# Exporting the Galaxy Catalogue:

df.to_csv(f'{path}/galaxy_catalogue_{area}.csv', mode='w', index=False, header=True)
