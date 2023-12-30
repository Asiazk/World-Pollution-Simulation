from Classes import Wind

MAP = ['SSSSSSSSSSSSSSSSSSSSSSSSS',
       'SSSSSSSSSSSSTTTTTTTTTSSSS',
       'LLLLSSSSSSSSSTTTTSSSSSSSS',
       'LLLLSSSSSSSSSSSSSSSSSSSSS',
       'SSSSSSSSSSSSSSSSSSSSSSSSS',
       'IIIISSSSSSSSSSSSSSSSSSSSS',
       'SSSSSSSSSSSSSSSSSSSSSSSSS',
       'TTTTFFFTTTTTTTTSSSSSSSSSS',
       'TTTTFFFFFFTTTTTSSSSSTTTTT',
       'SSSTTTTTTTTTTTTTSSSSSSSSS',
       'SSSSSSSSSSSSSSSSSSSSSSSSS',
       'SSLLLLLLLLSSSSSSSSSSSSSSS',
       'STTTTTTTSSSSSSSSTTTTTTTTT',
       'SSSSSSSSSSSSSSSSSSSSSSSSS',
       'SSSLLLLLLLLLLSSSSSSSSSSSS',
       'SSSSSSSSSSSSSSSSSSSSSSSSS',
       'SSSSSSSSSSSSSSSSSSSSSSSSS',
       'SSSSSSSSSSSSSSSSSSSSSSSSS',
       'SSIIIIIIIIIIIISSSSSSSSSSS',
       'IIIIIIIIIISSSSSIIIISSSSSS',
       'SSSSSSSSSSIIIIIIIIIISSSSS',
       'LLLLLLLLLSSSSSSSSSSSSSSSS',
       'SSSSSSSSSSSSSSSSSSSSSSSSS',
       'STTTTTTTSSSSSSSSSSSSSSSSS',
       'SSSTTTTTTTTTSSSSSSSSSSSSS']


WORLD_ROWS = 25
WORLD_COLUMNS = 25
DAYS_IN_YEAR = 365
CELL_SIZE = 40
ALIGN_CENTER = CELL_SIZE//2
MOVE_DOWN = 2.5
AIR_POLLUTION_INDEX = 0.03

# matching to the cell type: L S F I T
initialPollution1 = (1, 2, 1, 2, 6)
initialPollution2 = (3, 4, 3, 4, 8)
initialPollution3 = (5, 6, 5, 6, 10)
initialPollution4 = (1.1, 2.2, 1.1, 2.1, 6.1)
startingTemp = (18, 12, -10, 15, 21)
cloudRainStatuses = (1, 0, 0, 1, 1)
cellTypes = ('L', 'S', 'I', 'F', 'T')
directions = ('N', 'S', 'E', 'W', 'ST')  # North, South, East, West, Static
colors = ('#8B7D6B', '#007FFF', '#F0FFFF', '#3D9140', '#8470FF') # Land-Brown, Sea-Blue, Iceberg-White, Forest-Green, Town-Purple

def rotateMatrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]

WORLD_MAP = rotateMatrix(MAP)

winds1 = (Wind('N', 5), Wind('S', 7), Wind('E', 6), Wind('W', 4), Wind('N', 1))
winds2 = (Wind('S', 5), Wind('S', 5), Wind('N', 6), Wind('E', 3), Wind('W', 7))
