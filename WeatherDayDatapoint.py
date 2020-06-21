class WeatherDayDatapoint:
    def __init__( self, day, hTemp, lTemp, icon, precip):
        self.day = day;
        self.hTemp = hTemp;
        self.lTemp = lTemp;
        self.icon = icon;
        self.precip = precip;

    def setSunrise(self, sunrise):
        self.sunrise = sunrise

    def setSunset( self, sunset ):
        self.sunset = sunset
