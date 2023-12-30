class Wind:  # wind would change direction according to neighbors average
    def __init__(self, direction, intensity):
        self.direction = direction
        self.intensity = intensity

    def setDirection(self, newDirection):
        self.direction = newDirection

    def setIntensity(self, newIntensity):
        self.intensity = newIntensity

class Cell:
    def __init__(self, cellType, initialTemperature, currTemperature, wind, rainStatus, pollutionLevel, cloudStatus,
                 cellColor, row, col):
        self.cellType = cellType
        self.initialTemperature = initialTemperature
        self.currTemperature = currTemperature
        self.wind = wind
        self.rainStatus = rainStatus
        self.pollutionLevel = pollutionLevel
        self.cloudStatus = cloudStatus
        self.cellColor = cellColor
        self.row = row
        self.col = col

    def setTemperature(self, newTemperature):
        self.currTemperature = newTemperature

    def setWind(self, newWind):
        self.wind = newWind

    def setRainStatus(self, newRainStatus):
        self.rainStatus = newRainStatus

    def setPollution(self, newPollutionLevel):
        self.pollutionLevel = newPollutionLevel

    def setCloudStatus(self, newCloudStatus):
        self.cloudStatus = newCloudStatus

    def setToSea(self, seaType):
        self.cellType = seaType
