"""
    Simulation of pollution levels affects on average temperature
    The world is represented as biological automata
    Each cell can be part of: Land, Sea, Iceberg, Forest, Town
    Each cell has fields: Temperature, Wind (direction and intensity), Rain, Pollution, Cloud
    Each iteration = one day
    Conclusion: Higher pollution levels affect average temperature within time

    SW requirements: Python 3.9
    Run from command prompt from folder: Windows: Functions.py, Linux: python ./Functions.py
"""

from Functions import *

if __name__ == '__main__':
    pollutionList = []
    tempList =[]
    normPollutionList = []
    normTempList = []

    """
    first parameter of simulation can be changed to initialPollution2, initialPollution3, initialPollution4 
    and simulation will start with different initial pollution levels
    """
    simulation(initialPollution1, winds1, cloudRainStatuses, startingTemp, pollutionList, tempList)
    calculateStatisticsToText(tempList, "Temperatures_In_Year.txt", "Temperatures_In_Year_Normalized.txt", normTempList)
    calculateStatisticsToText(pollutionList, "Pollution_In_Year.txt", "Pollution_In_Year_Normalized.txt", normPollutionList)
    createGraph(tempList, normTempList, "Temperatures During The Year", "Days", "Temperatures")
    createGraph(pollutionList, normPollutionList, "Pollution levels During The Year", "Days", "Pollution Levels")
    calculatePearsonR(tempList, pollutionList)
