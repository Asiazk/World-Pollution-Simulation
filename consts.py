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

# -------------------- Default Configuration -------------------------
# matching to the cell type: L S F I T
INITIAL_POLLUTION_1 = (1, 2, 1, 2, 6)
INITIAL_POLLUTION_2 = (3, 4, 3, 4, 8)
INITIAL_POLLUTION_3 = (5, 6, 5, 6, 10)
INITIAL_POLLUTION_4 = (1.1, 2.2, 1.1, 2.1, 6.1)
STARTING_TEMP = (18, 12, -10, 15, 21)
CLOUD_RAIN_STATUSES = (1, 0, 0, 1, 1)
CELL_TYPES = ('L', 'S', 'I', 'F', 'T')
DIRECTIONS = ('N', 'S', 'E', 'W', 'ST')  # North, South, East, West, Static
COLORS = ('#8B7D6B', '#007FFF', '#F0FFFF', '#3D9140', '#8470FF') # Land-Brown, Sea-Blue, Iceberg-White, Forest-Green, Town-Purple
# --------------------------------------------------------------------
