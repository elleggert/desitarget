import os
from cuts import select_targets
import pandas as pd

filenames = []

path = 'bricks_data/tractor'
#path = '/Volumes/Astrostick/bricks_data/south/'


for filename in os.listdir(path):
    if '.fits' not in filename:
        continue
    filenames.append(f'{path}/{filename}')

res = select_targets(
    infiles=filenames, numproc=1, qso_selection='colorcuts', nside=None, gaiasub=False,
    tcnames=['LRG', 'ELG', 'QSO', 'LBG'], backup=False)



columns = []

# Check for later --> is overhead of converting to PD needed? Could go via Recarray immediately, ask Boris whether a CSV is needed
# Pipeline to go is: Run select_targets, convert to DF, extract desi_target bitcode, convert.
# Add cuts for Lyman Beak Galaxies, dropouts
# Extract SNRG --> ask Boris how
cols = [('RELEASE', '>i2'), ('BRICKID', '>i4'), ('BRICKNAME', 'S8'), ('BRICK_OBJID', '>i4'), ('MORPHTYPE', 'S4'), ('RA', '>f8'), ('RA_IVAR', '>f4'), ('DEC', '>f8'), ('DEC_IVAR', '>f4'), ('DCHISQ', '>f4', (5,)), ('EBV', '>f4'), ('FLUX_G', '>f4'), ('FLUX_R', '>f4'), ('FLUX_Z', '>f4'), ('FLUX_IVAR_G', '>f4'), ('FLUX_IVAR_R', '>f4'), ('FLUX_IVAR_Z', '>f4'), ('MW_TRANSMISSION_G', '>f4'), ('MW_TRANSMISSION_R', '>f4'), ('MW_TRANSMISSION_Z', '>f4'), ('FRACFLUX_G', '>f4'), ('FRACFLUX_R', '>f4'), ('FRACFLUX_Z', '>f4'), ('FRACMASKED_G', '>f4'), ('FRACMASKED_R', '>f4'), ('FRACMASKED_Z', '>f4'), ('FRACIN_G', '>f4'), ('FRACIN_R', '>f4'), ('FRACIN_Z', '>f4'), ('NOBS_G', '>i2'), ('NOBS_R', '>i2'), ('NOBS_Z', '>i2'), ('PSFDEPTH_G', '>f4'), ('PSFDEPTH_R', '>f4'), ('PSFDEPTH_Z', '>f4'), ('GALDEPTH_G', '>f4'), ('GALDEPTH_R', '>f4'), ('GALDEPTH_Z', '>f4'), ('FLUX_W1', '>f4'), ('FLUX_W2', '>f4'), ('FLUX_W3', '>f4'), ('FLUX_W4', '>f4'), ('FLUX_IVAR_W1', '>f4'), ('FLUX_IVAR_W2', '>f4'), ('FLUX_IVAR_W3', '>f4'), ('FLUX_IVAR_W4', '>f4'), ('MW_TRANSMISSION_W1', '>f4'), ('MW_TRANSMISSION_W2', '>f4'), ('MW_TRANSMISSION_W3', '>f4'), ('MW_TRANSMISSION_W4', '>f4'), ('ALLMASK_G', '>i2'), ('ALLMASK_R', '>i2'), ('ALLMASK_Z', '>i2'), ('FIBERFLUX_G', '>f4'), ('FIBERFLUX_R', '>f4'), ('FIBERFLUX_Z', '>f4'), ('FIBERTOTFLUX_G', '>f4'), ('FIBERTOTFLUX_R', '>f4'), ('FIBERTOTFLUX_Z', '>f4'), ('REF_EPOCH', '>f4'), ('WISEMASK_W1', 'u1'), ('WISEMASK_W2', 'u1'), ('MASKBITS', '>i2'), ('LC_FLUX_W1', '>f4', (15,)), ('LC_FLUX_W2', '>f4', (15,)), ('LC_FLUX_IVAR_W1', '>f4', (15,)), ('LC_FLUX_IVAR_W2', '>f4', (15,)), ('LC_NOBS_W1', '>i2', (15,)), ('LC_NOBS_W2', '>i2', (15,)), ('LC_MJD_W1', '>f8', (15,)), ('LC_MJD_W2', '>f8', (15,)), ('SHAPE_R', '>f4'), ('SHAPE_E1', '>f4'), ('SHAPE_E2', '>f4'), ('SHAPE_R_IVAR', '>f4'), ('SHAPE_E1_IVAR', '>f4'), ('SHAPE_E2_IVAR', '>f4'), ('SERSIC', '>f4'), ('SERSIC_IVAR', '>f4'), ('REF_ID', '>i8'), ('REF_CAT', 'S2'), ('GAIA_PHOT_G_MEAN_MAG', '>f4'), ('GAIA_PHOT_G_MEAN_FLUX_OVER_ERROR', '>f4'), ('GAIA_PHOT_BP_MEAN_MAG', '>f4'), ('GAIA_PHOT_BP_MEAN_FLUX_OVER_ERROR', '>f4'), ('GAIA_PHOT_RP_MEAN_MAG', '>f4'), ('GAIA_PHOT_RP_MEAN_FLUX_OVER_ERROR', '>f4'), ('GAIA_PHOT_BP_RP_EXCESS_FACTOR', '>f4'), ('GAIA_ASTROMETRIC_EXCESS_NOISE', '>f4'), ('GAIA_DUPLICATED_SOURCE', '?'), ('GAIA_ASTROMETRIC_SIGMA5D_MAX', '>f4'), ('GAIA_ASTROMETRIC_PARAMS_SOLVED', 'i1'), ('PARALLAX', '>f4'), ('PARALLAX_IVAR', '>f4'), ('PMRA', '>f4'), ('PMRA_IVAR', '>f4'), ('PMDEC', '>f4'), ('PMDEC_IVAR', '>f4'), ('PHOTSYS', '<U1'), ('TARGETID', '>i8'), ('DESI_TARGET', '>i8'), ('BGS_TARGET', '>i8'), ('MWS_TARGET', '>i8'), ('SUBPRIORITY', '>f8'), ('OBSCONDITIONS', '>i8'), ('PRIORITY_INIT_DARK', '>i8'), ('NUMOBS_INIT_DARK', '>i8'), ('PRIORITY_INIT_BRIGHT', '>i8'), ('NUMOBS_INIT_BRIGHT', '>i8'), ('PRIORITY_INIT_BACKUP', '>i8'), ('NUMOBS_INIT_BACKUP', '>i8')]

for c in cols:
    columns.append(c[0])


df = pd.DataFrame.from_records(data=list(res),columns=columns )

targets = df.DESI_TARGET.unique()

print(targets)

from targetmask import desi_mask

def desitarget_bitcode_2_str(bitcode):

    bina = (bin(bitcode))
    bina = bina[2:]

    desi_codes = []
    categories = []
    comments = []

    i = len(bina)-1
    for bit in bina:
        if bit == '1':
            desi_codes.append(i)
            comments.append(desi_mask.comment(i))
            categories.append(desi_mask.bitname(i))
        i -= 1

    return desi_codes,  categories, comments

for obj in targets:
    print(desitarget_bitcode_2_str(obj))

print(df.DESI_TARGET.value_counts())