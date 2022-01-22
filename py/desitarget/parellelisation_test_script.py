import os

import pandas as pd
from cuts import select_targets, format_output
import healpy as hp
import numpy as np

# ToDo:
# 2. Workout to store galaxy catalogue regardless of redshift information
# 3. Adapt script to accept CLArgs


# Defining important metrics and functions

# Setting NSIDE values
NSIDE = 256
NPIX = hp.nside2npix(NSIDE)


# Todo: check desitarget api if there is a equivalent function inside desitarget
def raDec2thetaPhi(ra, dec):
    return (0.5 * np.pi - np.deg2rad(dec)), (np.deg2rad(ra))


# Set path to where all northern bricks are
# path = '/Users/edgareggert/astrostatistics/bricks_data/tractor'
path = '/Volumes/Astrostick/bricks_data/south/'
area = 'south'
bricks_block_size = 100

# If using specific files for testing
# fn = ['tractor-0001m002.fits', 'tractor-1345p270.fits', 'tractor-2443p257.fits', 'tractor-3327p200.fits', 'tractor-1476m075.fits', 'tractor-3352m447.fits', 'tractor-3543p032.fits', 'tractor-0045m322.fits', 'tractor-1643p152.fits', 'tractor-0496m287.fits', 'tractor-1443p000.fits', 'tractor-0639m670.fits', 'tractor-2349p087.fits', 'tractor-0020m562.fits', 'tractor-3240m522.fits', 'tractor-2291p062.fits', 'tractor-2732p265.fits', 'tractor-1923p327.fits', 'tractor-3350p032.fits', 'tractor-2084p117.fits', 'tractor-3432p215.fits', 'tractor-0514m347.fits', 'tractor-3072m647.fits', 'tractor-1493m010.fits', 'tractor-1460p247.fits', 'tractor-0611m017.fits', 'tractor-2353p005.fits', 'tractor-2396p335.fits', 'tractor-1343m020.fits', 'tractor-0191p035.fits', 'tractor-1923m035.fits', 'tractor-0504m397.fits', 'tractor-0455m575.fits', 'tractor-0883m262.fits', 'tractor-1696p185.fits', 'tractor-2176m012.fits', 'tractor-2481p230.fits', 'tractor-0902m525.fits', 'tractor-0300p277.fits', 'tractor-0928m382.fits', 'tractor-1646m297.fits', 'tractor-0273p157.fits', 'tractor-0516m495.fits', 'tractor-0182m075.fits', 'tractor-0375m060.fits', 'tractor-1786p110.fits', 'tractor-0377m470.fits', 'tractor-1935p145.fits', 'tractor-0078p285.fits', 'tractor-0207p215.fits', 'tractor-0132m142.fits', 'tractor-2115m070.fits', 'tractor-1524p102.fits', 'tractor-0175p217.fits', 'tractor-2512p302.fits', 'tractor-2657p250.fits', 'tractor-1438m220.fits', 'tractor-0338m362.fits', 'tractor-0446m092.fits', 'tractor-1989m040.fits', 'tractor-2611p275.fits', 'tractor-0305m265.fits', 'tractor-1988p082.fits', 'tractor-0314m197.fits', 'tractor-0597m082.fits', 'tractor-1558p035.fits', 'tractor-0886m320.fits', 'tractor-2248m062.fits', 'tractor-0270m152.fits', 'tractor-1327p092.fits', 'tractor-2426p335.fits', 'tractor-0587m552.fits', 'tractor-1154p122.fits', 'tractor-2674p237.fits', 'tractor-3472m395.fits', 'tractor-0644m092.fits', 'tractor-1334p055.fits', 'tractor-1886m022.fits', 'tractor-0031p227.fits', 'tractor-2481p175.fits', 'tractor-1362p302.fits', 'tractor-3539p212.fits', 'tractor-3394p080.fits', 'tractor-3564p280.fits', 'tractor-0658m215.fits', 'tractor-0700m460.fits', 'tractor-0839m535.fits', 'tractor-0497m200.fits', 'tractor-0458m310.fits', 'tractor-0116m570.fits', 'tractor-2320p210.fits', 'tractor-1440p157.fits', 'tractor-3493m480.fits', 'tractor-1221p230.fits', 'tractor-0119p187.fits', 'tractor-0705m610.fits', 'tractor-0858m515.fits', 'tractor-1973m020.fits', 'tractor-0089p070.fits', 'tractor-0734m572.fits', 'tractor-0531m550.fits', 'tractor-1625p265.fits', 'tractor-0318m437.fits', 'tractor-1650p122.fits', 'tractor-1803p165.fits', 'tractor-3466p155.fits', 'tractor-1260p035.fits', 'tractor-1407p082.fits', 'tractor-1978p292.fits', 'tractor-2060p070.fits', 'tractor-0563m267.fits', 'tractor-2647p287.fits', 'tractor-2036m042.fits', 'tractor-3555p100.fits', 'tractor-1495p040.fits', 'tractor-0556m012.fits', 'tractor-3186m532.fits', 'tractor-1697p080.fits', 'tractor-1804p205.fits', 'tractor-1997p062.fits', 'tractor-0239m625.fits', 'tractor-0105m355.fits', 'tractor-1294m052.fits', 'tractor-3499p172.fits', 'tractor-3322p200.fits', 'tractor-3241p167.fits', 'tractor-1671p200.fits', 'tractor-3493m032.fits', 'tractor-0849m440.fits', 'tractor-2440p097.fits', 'tractor-2159m105.fits', 'tractor-0485m345.fits', 'tractor-2031p127.fits', 'tractor-3479p097.fits', 'tractor-0395p170.fits', 'tractor-2356p205.fits', 'tractor-2697p220.fits', 'tractor-0243m165.fits', 'tractor-3468p045.fits', 'tractor-2126p007.fits', 'tractor-0053m395.fits', 'tractor-0178m167.fits', 'tractor-1186p182.fits', 'tractor-1933m032.fits', 'tractor-1298m065.fits', 'tractor-0333m122.fits', 'tractor-1628m035.fits', 'tractor-1402p325.fits', 'tractor-0369p040.fits', 'tractor-3236m097.fits', 'tractor-2292p215.fits', 'tractor-2231p315.fits', 'tractor-1989p062.fits', 'tractor-1613p172.fits', 'tractor-3475p182.fits', 'tractor-0162m165.fits', 'tractor-1445p145.fits', 'tractor-0319m040.fits', 'tractor-3076m002.fits', 'tractor-0399m315.fits', 'tractor-0265p262.fits', 'tractor-1387p060.fits', 'tractor-0662m165.fits', 'tractor-1613m005.fits', 'tractor-0098m030.fits', 'tractor-0519m185.fits', 'tractor-2460p175.fits', 'tractor-0402m487.fits', 'tractor-2542p125.fits', 'tractor-2084p162.fits', 'tractor-2523p000.fits', 'tractor-0496p040.fits', 'tractor-0889m340.fits', 'tractor-2312p177.fits', 'tractor-2463p122.fits', 'tractor-0191p030.fits', 'tractor-1264m047.fits', 'tractor-0312p317.fits', 'tractor-1500m187.fits', 'tractor-0747m215.fits', 'tractor-0612m610.fits', 'tractor-0034m402.fits', 'tractor-0877m557.fits', 'tractor-0626m435.fits', 'tractor-0793m257.fits', 'tractor-3374p257.fits', 'tractor-2547p210.fits', 'tractor-2153p302.fits', 'tractor-2203p067.fits', 'tractor-0370m402.fits', 'tractor-1851p097.fits', 'tractor-0742m537.fits', 'tractor-0232m072.fits', 'tractor-2687p345.fits', 'tractor-0640m167.fits', 'tractor-1941p110.fits', 'tractor-0176m490.fits', 'tractor-2495p190.fits', 'tractor-2687p287.fits', 'tractor-0598m107.fits', 'tractor-2133m022.fits', 'tractor-0100p335.fits', 'tractor-0681m105.fits', 'tractor-1949p267.fits', 'tractor-3440p190.fits', 'tractor-3397p297.fits', 'tractor-3483p025.fits', 'tractor-1512p095.fits', 'tractor-1515p237.fits', 'tractor-1808m072.fits', 'tractor-1341p305.fits', 'tractor-2271p262.fits', 'tractor-2690p230.fits', 'tractor-2374p332.fits', 'tractor-3473p035.fits', 'tractor-1495p292.fits', 'tractor-1188m010.fits', 'tractor-0444m557.fits', 'tractor-1508p020.fits', 'tractor-2461p317.fits', 'tractor-0466p020.fits', 'tractor-1701p010.fits', 'tractor-1509p260.fits', 'tractor-0019p150.fits', 'tractor-1555p105.fits', 'tractor-0894m302.fits', 'tractor-1196p205.fits', 'tractor-3379p315.fits', 'tractor-0657m222.fits', 'tractor-3214m145.fits', 'tractor-0053m575.fits', 'tractor-3158m425.fits', 'tractor-0413m155.fits', 'tractor-0765m360.fits', 'tractor-1626m007.fits', 'tractor-0660m085.fits', 'tractor-0605m045.fits', 'tractor-1874p170.fits', 'tractor-2091m035.fits', 'tractor-3525p092.fits', 'tractor-1411p185.fits', 'tractor-1806p180.fits', 'tractor-0731m632.fits', 'tractor-1257p142.fits', 'tractor-0517m517.fits', 'tractor-0120m370.fits', 'tractor-1713p200.fits', 'tractor-0090m120.fits', 'tractor-3379m120.fits', 'tractor-2333p007.fits', 'tractor-0539m485.fits', 'tractor-3586p000.fits', 'tractor-1424p300.fits', 'tractor-3264p167.fits', 'tractor-1513p035.fits', 'tractor-1803p150.fits', 'tractor-1806p047.fits', 'tractor-3222p107.fits', 'tractor-1360p117.fits', 'tractor-1475m255.fits', 'tractor-0086p150.fits', 'tractor-0571m267.fits', 'tractor-0533m060.fits', 'tractor-3183p192.fits', 'tractor-3412m507.fits', 'tractor-3510p152.fits', 'tractor-2600p120.fits', 'tractor-0526m290.fits', 'tractor-1647p327.fits', 'tractor-0923m472.fits', 'tractor-3139p077.fits', 'tractor-1926m055.fits', 'tractor-0114m592.fits', 'tractor-1506p285.fits', 'tractor-2027p235.fits', 'tractor-2647p125.fits', 'tractor-0313m107.fits', 'tractor-3463p320.fits', 'tractor-0149m390.fits', 'tractor-0308p180.fits', 'tractor-0451m127.fits', 'tractor-1985p205.fits', 'tractor-2562p120.fits', 'tractor-0458m602.fits', 'tractor-0562m087.fits', 'tractor-1373p180.fits', 'tractor-1503p107.fits', 'tractor-0453m375.fits', 'tractor-3481m417.fits', 'tractor-2661p185.fits', 'tractor-1500p255.fits', 'tractor-0369m282.fits', 'tractor-2326p200.fits', 'tractor-3516m502.fits', 'tractor-1900p100.fits', 'tractor-0201m485.fits', 'tractor-1292p092.fits', 'tractor-0376m322.fits', 'tractor-3435m522.fits', 'tractor-2186p070.fits', 'tractor-0813m195.fits', 'tractor-1698p225.fits', 'tractor-0125p220.fits', 'tractor-2453p090.fits', 'tractor-0580m372.fits', 'tractor-3513p037.fits', 'tractor-1100p257.fits', 'tractor-3316p022.fits', 'tractor-3504p252.fits', 'tractor-2068p137.fits', 'tractor-3210m045.fits', 'tractor-3077m437.fits', 'tractor-1949p192.fits', 'tractor-0764m267.fits', 'tractor-2132p092.fits', 'tractor-1843m015.fits', 'tractor-0267m632.fits', 'tractor-2212p245.fits', 'tractor-0675m312.fits', 'tractor-1434p270.fits', 'tractor-0076p155.fits', 'tractor-0073p047.fits', 'tractor-2566p232.fits', 'tractor-0103p025.fits', 'tractor-3228m652.fits', 'tractor-3322m445.fits', 'tractor-0317p212.fits', 'tractor-2010p215.fits', 'tractor-1968p007.fits', 'tractor-1527m047.fits', 'tractor-0182p075.fits', 'tractor-2267m050.fits', 'tractor-0220p115.fits', 'tractor-0457m222.fits', 'tractor-2358p270.fits', 'tractor-0771m322.fits', 'tractor-0528m220.fits', 'tractor-3073m450.fits', 'tractor-0320p055.fits', 'tractor-3254m560.fits', 'tractor-3093p025.fits', 'tractor-0155m287.fits', 'tractor-0823m182.fits', 'tractor-0101p072.fits', 'tractor-1398m002.fits', 'tractor-0289m190.fits', 'tractor-1518m257.fits', 'tractor-3076m085.fits', 'tractor-3195p115.fits', 'tractor-0393m207.fits', 'tractor-2002p235.fits', 'tractor-0150m620.fits', 'tractor-2055p110.fits', 'tractor-1589p215.fits', 'tractor-2064p302.fits', 'tractor-1569p187.fits', 'tractor-0300p297.fits', 'tractor-3198m032.fits', 'tractor-1286m017.fits', 'tractor-0466p002.fits', 'tractor-0280m605.fits', 'tractor-1258p025.fits', 'tractor-0135p310.fits', 'tractor-3239m067.fits', 'tractor-3319p147.fits', 'tractor-3481m432.fits', 'tractor-0446m035.fits', 'tractor-0131m447.fits', 'tractor-2021p152.fits', 'tractor-3305p175.fits', 'tractor-0331p105.fits', 'tractor-1505p315.fits', 'tractor-2404p037.fits', 'tractor-3398m457.fits', 'tractor-2445p140.fits', 'tractor-2396p060.fits', 'tractor-0686m187.fits', 'tractor-1892p090.fits', 'tractor-1744p277.fits', 'tractor-0464p032.fits', 'tractor-0664m482.fits', 'tractor-0547m120.fits', 'tractor-1279p240.fits', 'tractor-2588p270.fits', 'tractor-3525p235.fits', 'tractor-1721p035.fits', 'tractor-2503p177.fits', 'tractor-1770p267.fits', 'tractor-0137p145.fits', 'tractor-0571m472.fits', 'tractor-1632m295.fits', 'tractor-1492p120.fits', 'tractor-0695m047.fits', 'tractor-0044m132.fits', 'tractor-2486p210.fits', 'tractor-3530m585.fits', 'tractor-1735p102.fits', 'tractor-0411p037.fits', 'tractor-1723m080.fits', 'tractor-0254p060.fits', 'tractor-0177m332.fits', 'tractor-3551m462.fits', 'tractor-1726p005.fits', 'tractor-2665p137.fits', 'tractor-0203p092.fits', 'tractor-1784p242.fits', 'tractor-3474p247.fits', 'tractor-2683p215.fits', 'tractor-0141m060.fits', 'tractor-3251m507.fits', 'tractor-0068p265.fits', 'tractor-3370m537.fits', 'tractor-3432p252.fits', 'tractor-3379p242.fits', 'tractor-1440p187.fits', 'tractor-3411m392.fits', 'tractor-0513m365.fits', 'tractor-0076p012.fits', 'tractor-0379m082.fits', 'tractor-0896m422.fits', 'tractor-3406p002.fits', 'tractor-0654m187.fits', 'tractor-1267m075.fits', 'tractor-3337p150.fits', 'tractor-1581m250.fits', 'tractor-1993p012.fits', 'tractor-3294p055.fits', 'tractor-3321m602.fits', 'tractor-1949p325.fits', 'tractor-0782m240.fits', 'tractor-0637m120.fits', 'tractor-2173m030.fits', 'tractor-1486p162.fits', 'tractor-0133p115.fits', 'tractor-2103p145.fits', 'tractor-0219p255.fits', 'tractor-2032p287.fits', 'tractor-3391p267.fits', 'tractor-1788m007.fits', 'tractor-3467p237.fits', 'tractor-0057m405.fits', 'tractor-3500p072.fits', 'tractor-2660p237.fits', 'tractor-0601m412.fits', 'tractor-2199p265.fits', 'tractor-0306p212.fits', 'tractor-1618p105.fits', 'tractor-3233m020.fits', 'tractor-3469p340.fits', 'tractor-0406p072.fits', 'tractor-3287p202.fits', 'tractor-1292m045.fits', 'tractor-0244m327.fits', 'tractor-2093p015.fits', 'tractor-0199p232.fits', 'tractor-0296m002.fits', 'tractor-0585m652.fits', 'tractor-2394p097.fits', 'tractor-3451m580.fits', 'tractor-0622m395.fits', 'tractor-2620p260.fits', 'tractor-0446m062.fits', 'tractor-1282p217.fits', 'tractor-3412m517.fits', 'tractor-2242m080.fits', 'tractor-1956p027.fits', 'tractor-1415m202.fits', 'tractor-0635m440.fits', 'tractor-2299p197.fits', 'tractor-3051m030.fits', 'tractor-1656p005.fits', 'tractor-0379m337.fits', 'tractor-2038m022.fits', 'tractor-0373m165.fits', 'tractor-0874m322.fits', 'tractor-0155p272.fits', 'tractor-1828m072.fits', 'tractor-2417p162.fits', 'tractor-0048m052.fits', 'tractor-1393p035.fits', 'tractor-0532m070.fits', 'tractor-0228p145.fits', 'tractor-1497m050.fits', 'tractor-0264m315.fits', 'tractor-1598p292.fits', 'tractor-1796m080.fits', 'tractor-1742p277.fits', 'tractor-0081m510.fits', 'tractor-1498m030.fits', 'tractor-1396m015.fits', 'tractor-3249p195.fits', 'tractor-1652p077.fits', 'tractor-3133m625.fits', 'tractor-3179m110.fits', 'tractor-3376m392.fits', 'tractor-0089m207.fits', 'tractor-0157p322.fits', 'tractor-0080m410.fits', 'tractor-0618m327.fits', 'tractor-3142p100.fits', 'tractor-1227m052.fits', 'tractor-1506m285.fits', 'tractor-0464m567.fits', 'tractor-3348p032.fits', 'tractor-3338p050.fits', 'tractor-1645m282.fits', 'tractor-2510p052.fits', 'tractor-2481p340.fits', 'tractor-2232p237.fits', 'tractor-3078m467.fits', 'tractor-0437m302.fits', 'tractor-2182m125.fits', 'tractor-0756m020.fits', 'tractor-1828p207.fits', 'tractor-1354p210.fits', 'tractor-0753m417.fits', 'tractor-3478m467.fits', 'tractor-3461p267.fits', 'tractor-0636m127.fits', 'tractor-0322m505.fits', 'tractor-1389p245.fits', 'tractor-1741m005.fits', 'tractor-0853m312.fits', 'tractor-2258p057.fits', 'tractor-0374m460.fits', 'tractor-0353m382.fits', 'tractor-0946m500.fits', 'tractor-2157p060.fits', 'tractor-0401m207.fits', 'tractor-2606p282.fits', 'tractor-1290p325.fits', 'tractor-3410p172.fits', 'tractor-2063p010.fits', 'tractor-1906p055.fits', 'tractor-1925p147.fits', 'tractor-0389p180.fits', 'tractor-3100p110.fits', 'tractor-2070p102.fits', 'tractor-2371p015.fits', 'tractor-3487m572.fits', 'tractor-0687m042.fits', 'tractor-3565p090.fits', 'tractor-1341p017.fits', 'tractor-3437p065.fits', 'tractor-0731m395.fits', 'tractor-1497p252.fits', 'tractor-0623m022.fits', 'tractor-3087m500.fits', 'tractor-3312m052.fits', 'tractor-1390m150.fits', 'tractor-2419p320.fits', 'tractor-0590m312.fits', 'tractor-0234m287.fits', 'tractor-0271m140.fits', 'tractor-0364m557.fits', 'tractor-0630m252.fits', 'tractor-0506p017.fits', 'tractor-2000m077.fits', 'tractor-1315p152.fits', 'tractor-3591p020.fits', 'tractor-0418p157.fits', 'tractor-0571m135.fits', 'tractor-1579m257.fits', 'tractor-2468p072.fits', 'tractor-0676m235.fits', 'tractor-2068p070.fits', 'tractor-0196m027.fits', 'tractor-0182m280.fits', 'tractor-1824p110.fits', 'tractor-1630p182.fits', 'tractor-2495p067.fits', 'tractor-0605m677.fits', 'tractor-0374m490.fits', 'tractor-0407m387.fits', 'tractor-0575m670.fits', 'tractor-0136m247.fits', 'tractor-0088p197.fits', 'tractor-0992m527.fits', 'tractor-0102p235.fits', 'tractor-3531p310.fits', 'tractor-0091m192.fits', 'tractor-3233p002.fits', 'tractor-2187p102.fits', 'tractor-1306m065.fits', 'tractor-3230m567.fits', 'tractor-2546p110.fits', 'tractor-2044p127.fits', 'tractor-3474p280.fits', 'tractor-0399m595.fits', 'tractor-0271m005.fits', 'tractor-0026p275.fits', 'tractor-0583m442.fits', 'tractor-1465m147.fits', 'tractor-0284m357.fits', 'tractor-1643p147.fits', 'tractor-1351p000.fits', 'tractor-1986m047.fits', 'tractor-0372p282.fits', 'tractor-3362p200.fits', 'tractor-0171p265.fits', 'tractor-0073m010.fits', 'tractor-1649p085.fits', 'tractor-3379m412.fits', 'tractor-2083m027.fits', 'tractor-3587m590.fits', 'tractor-0135m572.fits', 'tractor-2184p307.fits', 'tractor-3551m052.fits', 'tractor-0485m165.fits', 'tractor-0656m442.fits', 'tractor-1616m272.fits', 'tractor-3513p000.fits', 'tractor-0375p307.fits', 'tractor-1641p202.fits', 'tractor-2139p077.fits', 'tractor-1108p200.fits', 'tractor-2148p167.fits', 'tractor-0265m592.fits', 'tractor-0871m377.fits', 'tractor-1435p077.fits', 'tractor-2000p257.fits', 'tractor-3410m035.fits', 'tractor-2423p285.fits', 'tractor-1204m045.fits', 'tractor-2436p010.fits', 'tractor-1771m055.fits', 'tractor-1547m222.fits', 'tractor-1921p047.fits', 'tractor-1165p307.fits', 'tractor-0577m102.fits', 'tractor-1738p287.fits', 'tractor-1711p025.fits', 'tractor-0252m152.fits', 'tractor-0192m320.fits', 'tractor-2282p070.fits', 'tractor-3417p262.fits', 'tractor-0181m427.fits', 'tractor-1309m047.fits', 'tractor-3166m655.fits', 'tractor-0060m620.fits', 'tractor-0123p232.fits', 'tractor-2077p057.fits', 'tractor-1426m200.fits', 'tractor-0023p055.fits', 'tractor-0706m070.fits', 'tractor-0468m017.fits', 'tractor-1244p092.fits', 'tractor-2476p022.fits', 'tractor-0027m397.fits', 'tractor-2132m087.fits', 'tractor-0083p022.fits', 'tractor-0105p237.fits', 'tractor-2541p207.fits', 'tractor-0074p067.fits', 'tractor-2391p055.fits', 'tractor-0006p140.fits', 'tractor-3363m040.fits', 'tractor-0493m367.fits', 'tractor-3571m412.fits', 'tractor-3204m657.fits', 'tractor-1464p060.fits', 'tractor-0257m405.fits', 'tractor-3218p097.fits', 'tractor-0400m202.fits', 'tractor-1204p137.fits', 'tractor-0381p165.fits', 'tractor-0105m097.fits', 'tractor-0383p187.fits', 'tractor-0960m535.fits', 'tractor-1218p025.fits', 'tractor-1630p107.fits', 'tractor-0061m285.fits', 'tractor-0534m355.fits', 'tractor-0325m360.fits', 'tractor-3284m092.fits', 'tractor-0584m487.fits', 'tractor-1615m047.fits', 'tractor-3454m620.fits', 'tractor-0097p107.fits', 'tractor-1147p182.fits', 'tractor-1684p157.fits', 'tractor-0727m305.fits', 'tractor-3360m052.fits', 'tractor-3468p225.fits', 'tractor-3505p162.fits', 'tractor-0096p127.fits', 'tractor-1878m025.fits', 'tractor-3187p120.fits', 'tractor-0051p085.fits', 'tractor-2256p125.fits', 'tractor-3102m107.fits', 'tractor-0178m192.fits', 'tractor-3114m522.fits', 'tractor-2206p175.fits', 'tractor-0309p157.fits', 'tractor-3339m132.fits', 'tractor-3531p145.fits', 'tractor-1309m060.fits', 'tractor-1295p062.fits', 'tractor-2441p002.fits', 'tractor-0169p320.fits', 'tractor-2740p210.fits', 'tractor-3546m432.fits', 'tractor-0421m410.fits', 'tractor-3138p002.fits', 'tractor-1829p085.fits', 'tractor-1941m017.fits', 'tractor-0101m257.fits', 'tractor-0278m257.fits', 'tractor-0428m512.fits', 'tractor-2610p320.fits', 'tractor-3261m025.fits', 'tractor-1819p127.fits', 'tractor-0011p092.fits', 'tractor-1971m022.fits', 'tractor-1312p050.fits', 'tractor-3183p157.fits', 'tractor-2174m102.fits', 'tractor-3318p012.fits', 'tractor-2765p325.fits', 'tractor-3451m145.fits', 'tractor-1168p107.fits', 'tractor-0720m412.fits', 'tractor-0194p297.fits', 'tractor-3549p242.fits', 'tractor-0037m265.fits', 'tractor-2609p240.fits', 'tractor-0585m267.fits', 'tractor-0454m307.fits', 'tractor-0211m405.fits', 'tractor-0219p270.fits', 'tractor-1972p212.fits', 'tractor-0827m517.fits', 'tractor-2264m035.fits', 'tractor-2385p130.fits', 'tractor-0301p012.fits', 'tractor-3367p105.fits', 'tractor-3353p042.fits', 'tractor-0510m047.fits', 'tractor-0550m292.fits', 'tractor-0219m045.fits', 'tractor-1652p255.fits', 'tractor-0349m645.fits', 'tractor-0056p007.fits', 'tractor-1585m270.fits', 'tractor-0845m347.fits', 'tractor-0372p047.fits', 'tractor-1939m062.fits', 'tractor-2486p012.fits', 'tractor-1955p080.fits', 'tractor-0038m365.fits', 'tractor-2048m030.fits', 'tractor-1426p100.fits', 'tractor-3476p227.fits', 'tractor-2296p087.fits', 'tractor-0014m177.fits', 'tractor-1626p240.fits', 'tractor-3248m547.fits', 'tractor-0051m560.fits', 'tractor-1516m172.fits', 'tractor-3370m427.fits', 'tractor-0441m390.fits', 'tractor-0559m137.fits', 'tractor-1783p335.fits', 'tractor-0156m487.fits', 'tractor-1535m040.fits', 'tractor-1793m050.fits', 'tractor-0197m412.fits', 'tractor-3274m122.fits', 'tractor-0386m187.fits', 'tractor-0256p015.fits', 'tractor-1551p085.fits', 'tractor-0507m247.fits', 'tractor-2494p290.fits', 'tractor-0002m645.fits', 'tractor-2759p327.fits', 'tractor-0131p000.fits', 'tractor-1854p090.fits', 'tractor-0248m015.fits', 'tractor-3280p185.fits', 'tractor-2541p352.fits', 'tractor-1223p055.fits', 'tractor-1347p215.fits', 'tractor-0909m565.fits', 'tractor-1743p087.fits', 'tractor-2373p210.fits', 'tractor-1788p042.fits', 'tractor-3317p060.fits', 'tractor-1478p335.fits', 'tractor-2556p060.fits', 'tractor-3398p247.fits', 'tractor-3384m377.fits', 'tractor-0426p072.fits', 'tractor-0331m410.fits', 'tractor-1949p072.fits', 'tractor-0339m442.fits', 'tractor-0464m155.fits', 'tractor-3355m050.fits', 'tractor-0405p090.fits', 'tractor-0592m507.fits', 'tractor-1155p132.fits', 'tractor-3102p125.fits', 'tractor-0775m485.fits', 'tractor-1176p020.fits', 'tractor-0076p005.fits', 'tractor-2071p007.fits', 'tractor-3202m122.fits', 'tractor-0641m162.fits', 'tractor-0299m472.fits', 'tractor-0117m530.fits', 'tractor-1248p282.fits', 'tractor-1996m100.fits', 'tractor-1527p045.fits', 'tractor-3588p050.fits', 'tractor-2276p200.fits', 'tractor-0819m462.fits', 'tractor-0043m332.fits', 'tractor-0537m072.fits', 'tractor-0757m502.fits', 'tractor-3479m525.fits', 'tractor-2094m045.fits', 'tractor-1350p225.fits', 'tractor-3447m497.fits', 'tractor-2323p015.fits', 'tractor-1254p120.fits', 'tractor-3323p112.fits', 'tractor-0789m297.fits', 'tractor-3474m147.fits', 'tractor-3569m630.fits', 'tractor-1227p075.fits', 'tractor-0989m512.fits', 'tractor-0034p140.fits', 'tractor-0184m415.fits', 'tractor-2455p050.fits', 'tractor-0398p235.fits', 'tractor-1335p032.fits', 'tractor-0048p265.fits', 'tractor-2037p275.fits', 'tractor-0090p187.fits', 'tractor-0089m492.fits', 'tractor-1422m172.fits', 'tractor-2070p150.fits', 'tractor-3365m450.fits', 'tractor-3573m007.fits', 'tractor-0214m360.fits', 'tractor-1487p060.fits', 'tractor-1501p030.fits', 'tractor-1486p265.fits', 'tractor-2347p102.fits', 'tractor-3249m677.fits', 'tractor-1861m050.fits', 'tractor-0729m390.fits', 'tractor-1977p125.fits', 'tractor-3373m540.fits', 'tractor-2697p235.fits', 'tractor-0476m030.fits', 'tractor-1950p257.fits', 'tractor-3487m507.fits', 'tractor-1564p065.fits', 'tractor-1248p005.fits', 'tractor-1914p305.fits', 'tractor-3340p305.fits', 'tractor-2086p320.fits', 'tractor-2438p075.fits', 'tractor-1592m245.fits', 'tractor-1771m037.fits', 'tractor-3144m130.fits', 'tractor-0088m415.fits', 'tractor-3355m105.fits', 'tractor-2655p262.fits', 'tractor-0339m147.fits', 'tractor-3188m400.fits', 'tractor-0263m290.fits', 'tractor-0230p167.fits', 'tractor-3531m380.fits', 'tractor-0009m472.fits', 'tractor-3408m517.fits', 'tractor-0321p220.fits', 'tractor-0698m505.fits', 'tractor-0392p167.fits', 'tractor-0658m020.fits', 'tractor-3136m380.fits', 'tractor-1987p055.fits', 'tractor-3250m037.fits', 'tractor-3455p295.fits', 'tractor-1260m035.fits', 'tractor-2178p075.fits', 'tractor-0017p215.fits', 'tractor-3462m565.fits', 'tractor-1857p140.fits', 'tractor-0404m425.fits', 'tractor-0032m177.fits', 'tractor-3539p207.fits', 'tractor-1741m037.fits', 'tractor-0241p047.fits', 'tractor-0625m212.fits', 'tractor-2697p227.fits', 'tractor-0346m290.fits', 'tractor-3126m120.fits', 'tractor-0105m512.fits', 'tractor-0691m562.fits', 'tractor-1306m060.fits', 'tractor-3321p002.fits', 'tractor-1593m087.fits', 'tractor-0894m477.fits', 'tractor-0658m012.fits', 'tractor-2342p320.fits', 'tractor-3366m575.fits', 'tractor-1826p070.fits', 'tractor-1851p317.fits', 'tractor-0930m422.fits', 'tractor-2226m040.fits', 'tractor-1307p152.fits', 'tractor-2546p005.fits', 'tractor-2307p092.fits', 'tractor-0136m455.fits', 'tractor-0609m177.fits', 'tractor-2400p222.fits', 'tractor-1717m090.fits', 'tractor-2502p095.fits', 'tractor-3508p007.fits', 'tractor-1448m012.fits', 'tractor-1678p005.fits', 'tractor-1781p282.fits', 'tractor-0594m657.fits', 'tractor-3258m010.fits', 'tractor-1588m007.fits', 'tractor-0703m462.fits', 'tractor-1698p007.fits', 'tractor-0121m287.fits', 'tractor-1289p297.fits', 'tractor-1713m012.fits', 'tractor-0029m285.fits', 'tractor-2127m087.fits', 'tractor-0410m440.fits', 'tractor-2278p205.fits', 'tractor-0198p240.fits', 'tractor-3440p125.fits', 'tractor-2101p320.fits', 'tractor-1527m280.fits', 'tractor-3287m470.fits', 'tractor-3094m077.fits', 'tractor-1942p072.fits', 'tractor-2617p100.fits', 'tractor-0542m335.fits', 'tractor-3449m575.fits', 'tractor-0588m150.fits', 'tractor-3133m475.fits', 'tractor-1803p162.fits', 'tractor-3220p100.fits', 'tractor-0179m057.fits', 'tractor-2462p170.fits', 'tractor-2263m060.fits', 'tractor-2100p092.fits', 'tractor-3285m480.fits', 'tractor-1768p032.fits', 'tractor-1836p017.fits', 'tractor-0699m395.fits', 'tractor-0396m027.fits', 'tractor-0420m087.fits', 'tractor-1685m085.fits', 'tractor-0157p192.fits', 'tractor-3561m020.fits', 'tractor-3548m492.fits', 'tractor-0316p040.fits', 'tractor-3201m005.fits', 'tractor-3559p190.fits', 'tractor-3534m115.fits', 'tractor-0305p315.fits', 'tractor-0157m162.fits', 'tractor-0368p030.fits', 'tractor-3386p220.fits', 'tractor-3200m450.fits', 'tractor-1989p035.fits', 'tractor-2359p342.fits', 'tractor-0343m065.fits', 'tractor-0349m210.fits', 'tractor-1320p217.fits', 'tractor-0483p002.fits', 'tractor-0878m210.fits', 'tractor-3289p100.fits', 'tractor-0391p115.fits', 'tractor-2075m072.fits', 'tractor-2390p152.fits', 'tractor-0190m262.fits', 'tractor-0166p040.fits', 'tractor-0411m067.fits', 'tractor-3516p315.fits', 'tractor-3429p312.fits', 'tractor-0516m340.fits', 'tractor-3483p120.fits', 'tractor-0134m642.fits', 'tractor-1343p237.fits', 'tractor-1871m002.fits', 'tractor-1302p205.fits', 'tractor-0263m460.fits', 'tractor-3500p065.fits', 'tractor-0376m242.fits', 'tractor-3433m017.fits', 'tractor-1217p302.fits', 'tractor-0258m020.fits', 'tractor-1808m025.fits', 'tractor-0455p050.fits', 'tractor-3263p042.fits', 'tractor-0338m602.fits', 'tractor-1751m002.fits', 'tractor-3349m530.fits', 'tractor-1771p337.fits', 'tractor-2051p262.fits', 'tractor-2493p215.fits', 'tractor-1451p320.fits', 'tractor-1581p082.fits', 'tractor-0042m375.fits', 'tractor-0187p065.fits', 'tractor-2530p095.fits', 'tractor-0234p175.fits', 'tractor-0641m472.fits', 'tractor-3296m150.fits', 'tractor-0993m605.fits', 'tractor-0182p262.fits', 'tractor-1852p107.fits', 'tractor-3381p010.fits', 'tractor-3444m565.fits', 'tractor-1808p040.fits', 'tractor-3408p282.fits', 'tractor-3272p207.fits', 'tractor-3257p305.fits', 'tractor-2685p312.fits', 'tractor-1359m150.fits', 'tractor-3285p052.fits', 'tractor-3407m520.fits', 'tractor-1410p040.fits', 'tractor-3185p130.fits', 'tractor-0935m365.fits', 'tractor-0338m487.fits', 'tractor-2428p007.fits', 'tractor-1422m182.fits', 'tractor-0542m637.fits', 'tractor-3255p085.fits', 'tractor-3106m655.fits', 'tractor-1624p237.fits', 'tractor-0189p255.fits', 'tractor-3547m540.fits', 'tractor-2551p170.fits', 'tractor-0252p210.fits', 'tractor-2531p075.fits', 'tractor-3450m450.fits']
# filenames = [f'{path}/{filename}' for filename in fn]


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
