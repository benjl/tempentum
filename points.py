import utils

# Points you get for getting in a certain group (detialed in ttpoints)
wrpoints = 3000
# Points for the formula system - max points is factor_scale / (factor_smooth + 1)
factor_scale = 50000
factor_smooth = 49
# ttpoints determines what percentage of wrpoints you get
# -- Rank:    1,   2,    3,    4,     5,    6,    7,    8,    9,   10,   G1,   G2,     G3,    G4
ttpoints = (1.0, 0.75, 0.68, 0.61, 0.57, 0.53, 0.505, 0.48, 0.455, 0.43, 0.2, 0.13, 0.07, 0.03)

SCALE_FACTOR = (1, 1.5, 2, 2.5)
EXPONENT = (0.5, 0.56, 0.62, 0.68)
MINSIZE = (10, 45, 125, 250)

def points(rank, completions):
    return formula(rank) + group_points(rank, completions)
    
def groupsizes(completions):
    groupsize = []
    for i in range(4):
        groupsize.append(int(round(max(SCALE_FACTOR[i] * completions ** EXPONENT[i], MINSIZE[i]), 0)))
    return groupsize

def in_group(rank, completions):
    sizes = groupsizes(completions)
    g1_start = 11
    g2_start = g1_start + sizes[0]
    g3_start = g2_start + sizes[1]
    g4_start = g3_start + sizes[2]
    g4_end = g4_start + sizes[3]
    
    if rank <= 10:
        return 0
    if g1_start <= rank < g2_start:
        return 1
    if g2_start <= rank < g3_start:
        return 2
    if g3_start <= rank < g4_start:
        return 3
    if g4_start <= rank < g4_end:
        return 4
    else:
        return -1

def group_points(rank, completions):
    group = in_group(rank, completions)
    if group == 0:
        return ttpoints[rank-1] * wrpoints
    elif 1 <= group <= 4:
        return ttpoints[group+9] * wrpoints
    else:
        return 0

def formula(rank):
    return factor_scale / (factor_smooth + rank)