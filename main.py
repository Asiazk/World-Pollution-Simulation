"""
    Simulation of pollution levels affects on average temperature
    The world is represented as biological automata
    Each cell can be part of: Land, Sea, Iceberg, Forest, Town
    Each cell has fields: Temperature, Wind (direction and intensity), Rain, Pollution, Cloud
    Each iteration = one day

    SW requirements: Python 3.9
    Make sure all py files are in the same folder: main, gui, utils, consts, wind, cell
    Run from command prompt from folder: Windows: main.py, Linux: python ./main.py
"""

import utils
import consts
import wind
import gui


if __name__ == '__main__':
    pollutionList = []
    tempList =[]
    normPollutionList = []
    normTempList = []

    winds1 = (wind.Wind('N', 5), wind.Wind('S', 7), wind.Wind('E', 6), wind.Wind('W', 4), wind.Wind('N', 1))
    winds2 = (wind.Wind('S', 5), wind.Wind('S', 5), wind.Wind('N', 6), wind.Wind('E', 3), wind.Wind('W', 7))
    worldMap = utils.rotateMatrix(consts.MAP)

    """
    first parameter of simulation can be changed to initialPollution2, initialPollution3, initialPollution4 
    and simulation will start with different initial pollution levels
    """
    gui.simulation(consts.INITIAL_POLLUTION_1, winds1, consts.CLOUD_RAIN_STATUSES, consts.STARTING_TEMP, pollutionList, tempList, worldMap)
    utils.calculateStatisticsToText(tempList, "Temperatures_In_Year.txt", "Temperatures_In_Year_Normalized.txt", normTempList)
    utils.calculateStatisticsToText(pollutionList, "Pollution_In_Year.txt", "Pollution_In_Year_Normalized.txt", normPollutionList)
    gui.createGraph(tempList, normTempList, "Temperatures During The Year", "Days", "Temperatures")
    gui.createGraph(pollutionList, normPollutionList, "Pollution levels During The Year", "Days", "Pollution Levels")
    gui.calculatePearsonR(tempList, pollutionList)
