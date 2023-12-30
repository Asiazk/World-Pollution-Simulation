import time
import tkinter
import matplotlib.pyplot as plt
import numpy as np
import scipy
import statistics

import consts
import utils


# we collect the daily mean temperature and mean pollution levels into the lists in parameter
def simulation(initialPollution, initialWinds, initialCloudRain, startTemp, pollutionList, temperatureList, worldMap):
    root = tkinter.Tk()
    root.title("Simulation - Asia Zhivov")
    root.geometry("1200x1200")

    canvas = tkinter.Canvas(root, width=1000, height=1000)
    canvas.pack()
    daysLabel = tkinter.Label(root, text="Day 1", font=("Arial", 8, "bold"))
    daysLabel.pack()
    avgTempLabel = tkinter.Label(root, text="Average Temperature: ", font=("Arial", 8, "bold"))
    avgTempLabel.pack()
    avgPollution = tkinter.Label(root, text="Average Pollution: ", font=("Arial", 8, "bold"))
    avgPollution.pack()
    rectTextList = [[None for i in range(consts.WORLD_ROWS)] for j in range(consts.WORLD_COLUMNS)]
    rectList = [[None for i in range(consts.WORLD_ROWS)] for j in range(consts.WORLD_COLUMNS)]

    worldGrid = utils.createWorld(consts.WORLD_ROWS, consts.WORLD_COLUMNS, initialPollution, initialWinds, initialCloudRain, startTemp, worldMap)

    # create GUI
    for i in range(consts.WORLD_ROWS):
        for j in range(consts.WORLD_COLUMNS):
            currCell = worldGrid[i][j]
            currColor = currCell.cellColor
            cellSize = consts.CELL_SIZE
            alignCenter = consts.ALIGN_CENTER
            currRect = canvas.create_rectangle(i * cellSize, j * cellSize, (i + cellSize) * cellSize,
                                    (j + cellSize) * cellSize, fill=currColor, outline='black')
            rectText = canvas.create_text(i * cellSize + alignCenter, j * cellSize + alignCenter,
                                          text=currCell.currTemperature, fill='black', font=("Comic Sans MS", 8))
            rectTextList[i][j] = rectText
            rectList[i][j] = currRect

    for i in range(consts.DAYS_IN_YEAR):
        dayPollutionList = []
        dayTemperatureList = []
        daysLabel.config(text="Day " + str(i + 1))
        utils.calculateChangesInMap(worldGrid, dayPollutionList, dayTemperatureList)
        dailyMeanTemp = statistics.mean(dayTemperatureList)
        dailyMeanPol = statistics.mean(dayPollutionList)
        avgTempLabel.config(text="Average Temperature: " + str(round(dailyMeanTemp, 2)))
        avgPollution.config(text="Average Pollution: " + str(round(dailyMeanPol, 2)))
        pollutionList.append(dailyMeanPol)
        temperatureList.append(dailyMeanTemp)
        for j in range(consts.WORLD_ROWS):
            for k in range(consts.WORLD_COLUMNS):
                currentCell = worldGrid[j][k]
                canvas.itemconfig(rectTextList[j][k], text=currentCell.currTemperature)
                if utils.checkIceberg(worldGrid, j, k):
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


def createGraph(dataList, normDataList, fileName, xAxisLabel, yAxisLabel):
    X = [i+1 for i in range(consts.DAYS_IN_YEAR)]

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