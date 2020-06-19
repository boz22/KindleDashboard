class WeatherDatapoint:
    def __init__( self, hour, temperatureStr, iconStr, summaryStr, precipStr, windSpeed, windDirection, humidityStr, uvIndexStr ):
        self.hour = hour;
        self.temperature = temperatureStr
        self.icon = iconStr
        self.summary = summaryStr
        self.precip = precipStr
        self.windSpeed = windSpeed
        self.windDirection = windDirection
        self.humidity = humidityStr
        self.uvIndex = uvIndexStr
