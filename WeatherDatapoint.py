class WeatherDatapoint:
    def __init__( self, temperatureStr, iconStr, summaryStr, precipStr, windStr, humidityStr, uvIndexStr ):
        self.temperature = temperatureStr
        self.icon = iconStr
        self.summary = summaryStr
        self.precip = precipStr
        self.wind = windStr
        self.humidity = humidityStr
        self.uvIndex = uvIndexStr
