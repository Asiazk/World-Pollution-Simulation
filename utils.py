import statistics
import consts
import cell


def createWorld(rows, columns, initialPollution, initialWinds, cloudRainStatuses, startingTemp, worldMap):
    worldGrid = [[None for i in range(rows)] for j in range(columns)]

    for i in range(rows):
        for j in range(columns):
            currCellType = worldMap[i][j]
            currCellTypeIndex = consts.CELL_TYPES.index(currCellType)
            currWind = initialWinds[currCellTypeIndex]
            currCloud = cloudRainStatuses[currCellTypeIndex]
            currRainStatus = cloudRainStatuses[currCellTypeIndex]
            currPollution = initialPollution[currCellTypeIndex]
            currTemp = startingTemp[currCellTypeIndex]
            currColor = consts.COLORS[currCellTypeIndex]
            currCell = cell.Cell(cellType=currCellType, initialTemperature=currTemp, currTemperature=currTemp,
                            wind=currWind, rainStatus=currRainStatus, pollutionLevel=currPollution,
                            cloudStatus=currCloud, cellColor=currColor, row=i, col=j)
            worldGrid[i][j] = currCell
    return worldGrid


def findNeighbors(worldGrid, i, j):
    neighborsList = []
    if i - 1 >= 0:  # up
        neighborsList.append(worldGrid[i - 1][j])
    if i + 1 < len(worldGrid):  # down
        neighborsList.append(worldGrid[i + 1][j])
    if j - 1 >= 0:  # left
        neighborsList.append(worldGrid[i][j - 1])
    if j + 1 < len(worldGrid[0]):  # right
        neighborsList.append(worldGrid[i][j + 1])
    return neighborsList


def getStrongestWindNeighbor(worldGrid, i, j, neighborsList):
    mostIntenseCell = neighborsList[0]
    for neighbor in neighborsList:
        if neighbor.wind.intensity > mostIntenseCell.wind.intensity:
            mostIntenseCell = neighbor
    return mostIntenseCell


# The wind of each cell will change to most intense wind of all neighbors
def calculateWind(worldGrid, i, j, neighborsList):
    mostIntenseCell = neighborsList[0]
    for neighbor in neighborsList:
        if neighbor.wind.intensity > mostIntenseCell.wind.intensity:
            mostIntenseCell = neighbor

    worldGrid[i][j].wind.setDirection(mostIntenseCell.wind.direction)
    worldGrid[i][j].wind.setIntensity(mostIntenseCell.wind.intensity)
    newIntensity = mostIntenseCell.wind.intensity-0.009
    if newIntensity < 0:
        newIntensity = 0
    mostIntenseCell.wind.setIntensity(newIntensity)


# Rain will start if a cloud is present in cell and wind intensity is above 5
def calculateRain(worldGrid, i, j):
    if worldGrid[i][j].cloudStatus and worldGrid[i][j].wind.intensity > 5:
        worldGrid[i][j].rainStatus = 1
    else:
        worldGrid[i][j].rainStatus = 0


# The temperature of each cell will change according to the average temperature in the area, clouds, wind and rain
def calculateTemp(worldGrid, i, j, neighborsList):
    avgTemp = worldGrid[i][j].currTemperature
    finalTemp = worldGrid[i][j].currTemperature
    for neighbor in neighborsList:
        avgTemp += neighbor.currTemperature

    if worldGrid[i][j].currTemperature < avgTemp:
        finalTemp += 0.07
    if worldGrid[i][j].currTemperature > avgTemp:
        finalTemp -= 0.1
    if worldGrid[i][j].cloudStatus:
        finalTemp -= 0.01
    if worldGrid[i][j].wind.intensity > 5:
        finalTemp -= 0.2
    if worldGrid[i][j].pollutionLevel > 4:
        finalTemp += 0.01
    if worldGrid[i][j].rainStatus:
        finalTemp -= 0.8
    worldGrid[i][j].setTemperature(round(finalTemp, 2))
    return finalTemp


# Pollution level of each cell will change according to average in area and the wind
def calculatePollution(worldGrid, i, j, neighborsList):
    currPollution = worldGrid[i][j].pollutionLevel
    strongestWindNeighbor = getStrongestWindNeighbor(worldGrid, i, j, neighborsList)
    direction = strongestWindNeighbor.wind.direction
    if direction == 'N' and strongestWindNeighbor.row + 1 == i:
        currPollution += consts.AIR_POLLUTION_INDEX
    if direction == 'S' and strongestWindNeighbor.row - 1 == i:
        currPollution += consts.AIR_POLLUTION_INDEX
    if direction == 'W' and strongestWindNeighbor.col - 1 == j:
        currPollution += consts.AIR_POLLUTION_INDEX
    if direction == 'E' and strongestWindNeighbor.col + 1 == j:
        currPollution += consts.AIR_POLLUTION_INDEX
    if currPollution > 10:
        currPollution = 10
    worldGrid[i][j].setPollution(currPollution)
    return currPollution


# Clouds move according to strongest wind direction
def calculateCloud(worldGrid, i, j, neighborsList):
    strongest = getStrongestWindNeighbor(worldGrid, i, j, neighborsList)
    direction = strongest.wind.direction
    if strongest.cloudStatus:
        if direction == 'N' and strongest.row + 1 == i:
            worldGrid[i][j].cloudStatus = 1
        if direction == 'S' and strongest.row - 1 == i:
            worldGrid[i][j].cloudStatus = 1
        if direction == 'W' and strongest.col - 1 == j:
            worldGrid[i][j].cloudStatus = 1
        if direction == 'E' and strongest.col + 1 == j:
            worldGrid[i][j].cloudStatus = 1


def calculateChangesInMap(worldGrid, pollutionList, temperatureList):
    for i in range(len(worldGrid)):
        for j in range(len(worldGrid[0])):
            currNeighborsList = findNeighbors(worldGrid, i, j)
            getStrongestWindNeighbor(worldGrid, i, j, currNeighborsList)
            calculateWind(worldGrid, i, j, currNeighborsList)
            pollutionList.append(calculatePollution(worldGrid, i, j, currNeighborsList))
            calculateCloud(worldGrid, i, j, currNeighborsList)
            calculateRain(worldGrid, i, j)
            temperatureList.append(calculateTemp(worldGrid, i, j, currNeighborsList))


def checkIceberg(worldGrid, i, j):
    if worldGrid[i][j].cellType == 'I' and int(worldGrid[i][j].currTemperature) >= 0:
        worldGrid[i][j].setToSea('S')
        return True
    return False


# calculate statistics of temperature and pollution and write in txt file
def calculateStatisticsToText(itemList, fileNameData, fileNameNormData, itemListNorm):
    average = statistics.mean(itemList)
    averageSD = statistics.pstdev(itemList)
    dataInYear = open(fileNameData, "w")
    dataInYearNorm = open(fileNameNormData, "w")
    for item in itemList:
        dataInYear.write("{}\n".format(item))
        dataNorm = (item - average) / averageSD
        itemListNorm.append(dataNorm)
        dataInYearNorm.write("{}\n".format(dataNorm))
    dataInYear.close()
    dataInYearNorm.close()


def rotateMatrix(m):
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]) - 1, -1, -1)]
