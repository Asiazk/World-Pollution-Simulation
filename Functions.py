import time
import tkinter
from tkinter import *
import statistics
import matplotlib.pyplot as plt
import numpy as np
import scipy
from Constants import *
from Classes import Wind, Cell


def createWorld(rows, columns, initialPollution, initialWinds, cloudRainStatuses, startingTemp):
    worldGrid = [[None for i in range(rows)] for j in range(columns)]

    for i in range(rows):
        for j in range(columns):
            currCellType = WORLD_MAP[i][j]
            currCellTypeIndex = cellTypes.index(currCellType)
            currWind = initialWinds[currCellTypeIndex]
            currCloud = cloudRainStatuses[currCellTypeIndex]
            currRainStatus = cloudRainStatuses[currCellTypeIndex]
            currPollution = initialPollution[currCellTypeIndex]
            currTemp = startingTemp[currCellTypeIndex]
            currColor = colors[currCellTypeIndex]
            currCell = Cell(cellType=currCellType, initialTemperature=currTemp, currTemperature=currTemp,
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
        currPollution += AIR_POLLUTION_INDEX
    if direction == 'S' and strongestWindNeighbor.row - 1 == i:
        currPollution += AIR_POLLUTION_INDEX
    if direction == 'W' and strongestWindNeighbor.col - 1 == j:
        currPollution += AIR_POLLUTION_INDEX
    if direction == 'E' and strongestWindNeighbor.col + 1 == j:
        currPollution += AIR_POLLUTION_INDEX
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


# we collect the daily mean temperature and mean pollution levels into the lists in parameter
def simulation(initialPollution, initialWinds, initialCloudRain, startTemp, pollutionList, temperatureList):
    root = Tk()
    root.title("Simulation - Asia Zhivov")
    root.geometry("1200x1200")

    canvas = tkinter.Canvas(root, width=1000, height=1000)
    canvas.pack()
    daysLabel = Label(root, text="Day 1", font=("Arial", 8, "bold"))
    daysLabel.pack()
    avgTempLabel = Label(root, text="Average Temperature: ", font=("Arial", 8, "bold"))
    avgTempLabel.pack()
    avgPollution = Label(root, text="Average Pollution: ", font=("Arial", 8, "bold"))
    avgPollution.pack()
    rectTextList = [[None for i in range(WORLD_ROWS)] for j in range(WORLD_COLUMNS)]
    rectList = [[None for i in range(WORLD_ROWS)] for j in range(WORLD_COLUMNS)]

    worldGrid = createWorld(WORLD_ROWS, WORLD_COLUMNS, initialPollution, initialWinds, initialCloudRain, startTemp)

    # create GUI
    for i in range(WORLD_ROWS):
        for j in range(WORLD_COLUMNS):
            currCell = worldGrid[i][j]
            currColor = currCell.cellColor
            currRect = canvas.create_rectangle(i * CELL_SIZE, j * CELL_SIZE, (i + CELL_SIZE) * CELL_SIZE,
                                    (j + CELL_SIZE) * CELL_SIZE, fill=currColor, outline='black')
            rectText = canvas.create_text(i * CELL_SIZE + ALIGN_CENTER, j * CELL_SIZE + ALIGN_CENTER,
                                          text=currCell.currTemperature, fill='black', font=("Comic Sans MS", 8))
            rectTextList[i][j] = rectText
            rectList[i][j] = currRect

    for i in range(DAYS_IN_YEAR):
        dayPollutionList = []
        dayTemperatureList = []
        daysLabel.config(text="Day " + str(i + 1))
        calculateChangesInMap(worldGrid, dayPollutionList, dayTemperatureList)
        dailyMeanTemp = statistics.mean(dayTemperatureList)
        dailyMeanPol = statistics.mean(dayPollutionList)
        avgTempLabel.config(text="Average Temperature: " + str(round(dailyMeanTemp, 2)))
        avgPollution.config(text="Average Pollution: " + str(round(dailyMeanPol, 2)))
        pollutionList.append(dailyMeanPol)
        temperatureList.append(dailyMeanTemp)
        for j in range(WORLD_ROWS):
            for k in range(WORLD_COLUMNS):
                currentCell = worldGrid[j][k]
                canvas.itemconfig(rectTextList[j][k], text=currentCell.currTemperature)
                if checkIceberg(worldGrid, j, k):
                    canvas.itemconfig(rectList[j][k], fill='#007FFF')
                if i % 10 == 0:  # add new clouds and winds every 10 days raise pollution in towns
                    if k == 24:
                        currentCell.setCloudStatus(1)
                        currentCell.wind.setDirection('W')
                        currentCell.wind.setIntensity(5)
                    if currentCell.cellType == 'T':
                        newPolLevel = currentCell.pollutionLevel + 2
                        if newPolLevel > 10:
                            newPolLevel = 10
                        currentCell.setPollution(newPolLevel)
        # time.sleep(1) # you can change the delay between days
        canvas.update()
    time.sleep(5)
    root.destroy()
    root.mainloop()

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


def createGraph(dataList, normDataList, fileName, xAxisLabel, yAxisLabel):
    X = [i+1 for i in range(DAYS_IN_YEAR)]

    x1 = np.array(X)
    y1 = np.array(dataList)
    x1n = np.array(X)
    y1n = np.array(normDataList)
    plt.plot(x1, y1, c='g')
    plt.plot(x1n, y1n, c='b')
    plt.title(fileName + "(green - average, blue - normalized)")
    plt.xlabel(xAxisLabel)
    plt.ylabel(yAxisLabel)
    plt.savefig(fileName + '.png')
    plt.show()
    plt.clf()


def calculatePearsonR(dataList1, dataList2):
    # correlation
    y2 = np.array(dataList1)
    y1 = np.array(dataList2)
    r = scipy.stats.pearsonr(y1,y2)
    pearsonR = open("pearsonR.txt", "w")
    pearsonR.write(str(r))
    pearsonR.close()
