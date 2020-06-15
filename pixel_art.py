NUL = [0, 0, 0]

BLK = [15, 15, 15]    # https://rgbcolorcode.com/color/black
LBU = [173, 216, 230] # https://rgbcolorcode.com/color/light-blue
BLU = [0, 0, 255]     # https://rgbcolorcode.com/color/blue
BRN = [150, 75, 0]    # https://rgbcolorcode.com/color/brown
GLD = [128, 128, 0]   # https://rgbcolorcode.com/color/heart-gold
GRN = [0, 255, 0]     # https://rgbcolorcode.com/color/green
GRY = [128, 128, 128] # https://rgbcolorcode.com/color/gray
LPK = [255, 192, 203] # https://rgbcolorcode.com/color/pink
PNK = [255, 0, 255]   # https://rgbcolorcode.com/color/fuchsia
RED = [255, 0, 0]     # https://rgbcolorcode.com/color/red
TAN = [210, 180, 140] # https://rgbcolorcode.com/color/tan 
YEL = [255, 255, 0]   # https://rgbcolorcode.com/color/yellow
SLV = [192, 192, 192] # https://rgbcolorcode.com/color/silver
WHT = [255, 255, 255] # https://rgbcolorcode.com/color/white

template = [
    NUL, NUL, NUL, NUL, NUL, NUL, NUL, NUL,
    NUL, NUL, NUL, NUL, NUL, NUL, NUL, NUL,
    NUL, NUL, NUL, NUL, NUL, NUL, NUL, NUL,
    NUL, NUL, NUL, NUL, NUL, NUL, NUL, NUL,
    NUL, NUL, NUL, NUL, NUL, NUL, NUL, NUL,
    NUL, NUL, NUL, NUL, NUL, NUL, NUL, NUL,
    NUL, NUL, NUL, NUL, NUL, NUL, NUL, NUL,
    NUL, NUL, NUL, NUL, NUL, NUL, NUL, NUL
]

snake = [
    NUL, NUL, NUL, NUL, NUL, NUL, NUL, GRN,
    NUL, GRN, GRN, GRN, GRN, GRN, GRN, GRN,
    NUL, GRN, NUL, NUL, NUL, NUL, NUL, NUL,
    NUL, GRN, GRN, GRN, GRN, GRN, NUL, NUL,
    NUL, NUL, NUL, NUL, NUL, GRN, NUL, NUL,
    BLU, GRN, BLU, GRN, GRN, GRN, NUL, NUL,
    GRN, GRN, GRN, NUL, NUL, NUL, NUL, NUL,
    RED, NUL, NUL, NUL, NUL, NUL, NUL, NUL
]

link = [
    NUL, GRN, GRN, GRN, GRN, NUL, SLV, NUL,
    NUL, GRN, GRN, GRN, GRN, NUL, SLV, NUL,
    NUL, TAN, BLK, TAN, BLK, NUL, SLV, NUL,
    NUL, TAN, TAN, TAN, TAN, NUL, SLV, NUL,
    BRN, BRN, GRN, GRN, GRN, BLU, BLU, BLU,
    BRN, BRN, GRN, GRN, GRN, TAN, TAN, NUL,
    BRN, BRN, GRN, GRN, GRN, NUL, BLU, NUL,
    NUL, BLK, NUL, NUL, BLK, NUL, NUL, NUL
]

kirby = [
    NUL, NUL, NUL, LPK, LPK, LPK, NUL, NUL,
    NUL, NUL, LPK, NUL, LPK, NUL, LPK, NUL,
    NUL, LPK, LPK, NUL, LPK, NUL, LPK, NUL,
    LPK, LPK, PNK, PNK, LPK, PNK, PNK, LPK,
    LPK, LPK, LPK, LPK, NUL, LPK, LPK, LPK,
    NUL, LPK, LPK, LPK, LPK, LPK, LPK, LPK,
    NUL, NUL, LPK, LPK, LPK, LPK, LPK, NUL,
    NUL, PNK, PNK, PNK, NUL, PNK, PNK, PNK
]

fallout_boy = [
    NUL, NUL, YEL, YEL, YEL, YEL, NUL, NUL,
    NUL, YEL, TAN, TAN, TAN, TAN, NUL, BRN,
    NUL, TAN, TAN, BLK, TAN, BLK, NUL, BRN,
    NUL, TAN, TAN, TAN, TAN, TAN, NUL, RED,
    BLU, BLU, BLU, YEL, BLU, BLU, BLU, TAN,
    TAN, BLU, BLU, YEL, BLU, BLU, NUL, BRN,
    NUL, BLU, BLU, GLD, BLU, BLU, NUL, NUL,
    NUL, BLK, NUL, NUL, NUL, BLK, NUL, NUL
]

si_sm_squid_0 = [
    NUL, NUL, NUL, PNK, PNK, NUL, NUL, NUL,
    NUL, NUL, PNK, PNK, PNK, PNK, NUL, NUL,
    NUL, PNK, PNK, PNK, PNK, PNK, PNK, NUL,
    PNK, PNK, NUL, PNK, PNK, NUL, PNK, PNK,
    PNK, PNK, PNK, PNK, PNK, PNK, PNK, PNK,
    NUL, NUL, PNK, NUL, NUL, PNK, NUL, NUL,
    NUL, PNK, NUL, PNK, PNK, NUL, PNK, NUL,
    PNK, NUL, PNK, NUL, NUL, PNK, NUL, PNK
]

si_sm_squid_1 = [
    NUL, NUL, NUL, PNK, PNK, NUL, NUL, NUL,
    NUL, NUL, PNK, PNK, PNK, PNK, NUL, NUL,
    NUL, PNK, PNK, PNK, PNK, PNK, PNK, NUL,
    PNK, PNK, NUL, PNK, PNK, NUL, PNK, PNK,
    PNK, PNK, PNK, PNK, PNK, PNK, PNK, PNK,
    NUL, PNK, NUL, PNK, PNK, NUL, PNK, NUL,
    PNK, NUL, NUL, NUL, NUL, NUL, NUL, PNK,
    NUL, PNK, NUL, NUL, NUL, NUL, PNK, NUL
]

si_med_crab_0 = [
    NUL, BLU, NUL, NUL, NUL, NUL, BLU, NUL,
    NUL, NUL, BLU, NUL, NUL, BLU, NUL, NUL,
    NUL, BLU, BLU, BLU, BLU, BLU, BLU, NUL,
    BLU, BLU, NUL, BLU, BLU, NUL, BLU, BLU,
    BLU, BLU, BLU, BLU, BLU, BLU, BLU, BLU,
    NUL, BLU, BLU, BLU, BLU, BLU, BLU, NUL,
    NUL, BLU, NUL, NUL, NUL, NUL, BLU, NUL,
    NUL, NUL, BLU, NUL, NUL, BLU, NUL, NUL
]

si_med_crab_1 = [
    NUL, BLU, NUL, NUL, NUL, NUL, BLU, NUL,
    NUL, NUL, BLU, NUL, NUL, BLU, NUL, NUL,
    NUL, BLU, BLU, BLU, BLU, BLU, BLU, NUL,
    BLU, BLU, NUL, BLU, BLU, NUL, BLU, BLU,
    BLU, BLU, BLU, BLU, BLU, BLU, BLU, BLU,
    NUL, BLU, BLU, BLU, BLU, BLU, BLU, NUL,
    NUL, NUL, BLU, NUL, NUL, BLU, NUL, NUL,
    NUL, BLU, NUL, NUL, NUL, NUL, BLU, NUL
]

si_lrg_octopus_0 = [
    NUL, NUL, NUL, YEL, YEL, NUL, NUL, NUL,
    NUL, YEL, YEL, YEL, YEL, YEL, YEL, NUL,
    YEL, YEL, YEL, YEL, YEL, YEL, YEL, YEL,
    YEL, NUL, NUL, YEL, YEL, NUL, NUL, YEL,
    YEL, YEL, YEL, YEL, YEL, YEL, YEL, YEL,
    NUL, NUL, YEL, NUL, NUL, YEL, NUL, NUL,
    NUL, YEL, NUL, YEL, YEL, NUL, YEL, NUL,
    YEL, NUL, NUL, NUL, NUL, NUL, NUL, YEL
]

si_lrg_octopus_1 = [
    NUL, NUL, NUL, YEL, YEL, NUL, NUL, NUL,
    NUL, YEL, YEL, YEL, YEL, YEL, YEL, NUL,
    YEL, YEL, YEL, YEL, YEL, YEL, YEL, YEL,
    YEL, NUL, NUL, YEL, YEL, NUL, NUL, YEL,
    YEL, YEL, YEL, YEL, YEL, YEL, YEL, YEL,
    NUL, YEL, YEL, NUL, NUL, YEL, YEL, NUL,
    YEL, NUL, NUL, YEL, YEL, NUL, NUL, YEL,
    NUL, YEL, NUL, NUL, NUL, NUL, YEL, NUL
]