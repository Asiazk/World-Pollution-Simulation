class Wind:  # wind would change direction according to neighbors average
    def __init__(self, direction, intensity):
        self.direction = direction
        self.intensity = intensity

    def setDirection(self, newDirection):
        self.direction = newDirection

    def setIntensity(self, newIntensity):
        self.intensity = newIntensity
