from WeatherDatapoint import WeatherDatapoint
from WeatherDayDatapoint import WeatherDayDatapoint
from typing import List
import requests
from bs4 import BeautifulSoup
from svg_normalize import inlineSvg
from weather_utils import convert_fahrenheit_to_celsius
from weather_utils import degree_sign
from weather_utils import convert_miles_to_km
from svg_normalize import convertSvgToPng
from images_utils import base64_add_png_mimetype
from images_utils import to_base64

class WeatherComProvider:
    def __init__( self ):
        #TODO: Figure out URL by providing the location or latitude, longitude
        self.hourByHourUrl = "https://weather.com/weather/hourbyhour/l/528bd2c6382325ac2a6194902c8d73cd603a32bee30cef6a16447b533486a83d"
        self.dailyUrl = "https://weather.com/weather/today/l/528bd2c6382325ac2a6194902c8d73cd603a32bee30cef6a16447b533486a83d"

    """
    Returns a list with objects, each object representing the forecast for a day
    """
    def getDaily(self):
        print('Retrieving daily forecast...')
        print('Requesting page: ' + self.dailyUrl)
        page = requests.get(self.dailyUrl)
        days = self.__getDailyDatapoints( page.text )
        return days

    def getHourByHour(self) -> List:
        print('Retrieving hour by hour forecacst')
        print('Requesting page: ' + self.hourByHourUrl)
        page = requests.get(self.hourByHourUrl)
        datapoints = self.getDatapoints( page.text )
        return datapoints


    def __getDailyDatapoints( self, htmlText ):
        soup = BeautifulSoup(htmlText, 'html.parser')
        section = soup.find("section", attrs={ 'data-testid': 'DailyWeatherModule' });
        daysListElem = section.find("ul", attrs={ 'data-testid': 'WeatherTable' });
        days = daysListElem.find_all("li");
        daysDp = []
        for day in days:
            dayLabel = day.find("h3").get_text()
            highTemp = day.find("div", attrs={ 'data-testid': 'SegmentHighTemp' }).get_text()
            if "-" not in highTemp:
                highTemp = self.convertToCelsius(highTemp) + degree_sign
            lowTemp = day.find("div", attrs={ 'data-testid': 'SegmentLowTemp' }).get_text()
            lowTemp = self.convertToCelsius(lowTemp) + degree_sign
            icon = day.find("svg");
            icon['xmlns:xlink'] = "http://www.w3.org/1999/xlink"
            icon = inlineSvg( icon, soup )
            iconBase64 = self.convertIconToBase64( str(icon) );
            precip = day.find("div", attrs={ 'data-testid': 'SegmentPrecipPercentage' }).get_text()
            dayDp = WeatherDayDatapoint(dayLabel, highTemp, lowTemp, iconBase64, precip)
            daysDp.append(dayDp)

        #The first element of the list with today, so we use the same page to retrieve the sunrise and sunset for today
        todaySection = soup.find("section", attrs={ 'data-testid': 'TodaysDetailsModule' });
        sunriseValue = todaySection.find("div", attrs={ 'data-testid': 'SunriseValue' }).get_text();
        sunsetValue = todaySection.find("div", attrs={ 'data-testid': 'SunsetValue' }).get_text();
        daysDp[0].setSunrise( sunriseValue )
        daysDp[0].setSunset( sunsetValue )
        return daysDp

    def getDatapoints(self, htmlText):
        print('Building list with hourly datapoints')
        print('Parsing the page...')
        soup = BeautifulSoup(htmlText, 'html.parser')
        section = soup.find("section", attrs={ 'data-testid': 'HourlyForecast' });
        detailsSections = section.select("details");
        dpList = []
        print('Iterating through all detail sections')
        for detailSection in detailsSections:
            #Summary card
            detailSummary = detailSection.find("summary")
            hour = detailSummary.find('h2', attrs={ 'data-testid': 'daypartName' })
            temperature = detailSummary.find('span', attrs={ 'data-testid': 'TemperatureValue' })
            iconAndSummary = detailSummary.find('div', attrs={ 'data-testid': 'wxIcon' })
            icon = iconAndSummary.find("svg");
            icon['xmlns:xlink'] = "http://www.w3.org/1999/xlink"
            #icon = inlineSvg( icon, soup )
            summary = iconAndSummary.find("span")
            precip = detailSummary.find('span', attrs={ 'data-testid': 'PercentageValue' })
            wind = detailSummary.find('span', attrs={ 'data-testid': 'Wind' })

            #Details card
            ulDetails = detailSection.find('ul', attrs={ 'data-testid': 'DetailsTable' })
            humidity = ulDetails.find("span", attrs={'data-testid': 'PercentageValue'})
            uvIndex = ulDetails.find("span", attrs={'data-testid': 'UVIndexValue'})

            #Build datapoint
            dp = self.buildHourlyDatapoint( hour, temperature, icon, summary, precip, wind, humidity, uvIndex )
            dpList.append( dp )
        return dpList

    """
    Hours will be expressed in 0-23 numbers (not 21:00, but 21);
    Temperature in Celsius;
    Wind speed in kmh;
    Humidity in percentage;
    uv index in numbers from 1 to 10;
    """
    def buildHourlyDatapoint(self, hour, temperature, icon, summary, precip, wind, humidity, uvIndex ):
        hourStr = hour.text
        hourStr = self.convertHour24hFormat(hourStr)
        temperatureStr = temperature.text
        temperatureStr = self.convertToCelsius( temperatureStr )
        iconStr = str(icon)
        #iconStr = self.convertIconToBase64( iconStr )
        summaryStr = summary.text
        precipStr = precip.text
        precipStr = precipStr[:-1]
        windStr = wind.text
        windSpeed, windDirection = self.getWindSpeedAndDirection( windStr )
        windSpeed = str(int( convert_miles_to_km((int( windSpeed ) )) ))
        humidityStr = humidity.text
        humidityStr = humidityStr[:-1]
        uvIndexStr = uvIndex.text
        uvIndexStr = self.convertUvIndexToNumber( uvIndexStr )
        datapoint = WeatherDatapoint( hourStr, temperatureStr, iconStr, summaryStr, precipStr, windSpeed, windDirection, humidityStr, uvIndexStr )
        return datapoint


    """
    Given a string like 3 of 10 it will remove the scale and return only the index (i.e: 3)
    """
    def convertUvIndexToNumber(self, uvIndexStr):
        uvIndexArr = uvIndexStr.split()
        if len(uvIndexArr) == 3:
            return uvIndexArr[0]

    """
    Given an hour string like 8 am or 9 pm it will convert it into 24h format (i.e: 8 or 21 respectively)
    """
    def convertHour24hFormat(self, hourStr ):
        hourArr = hourStr.split();
        hour = hourArr[0]
        meridian = hourArr[1]
        if hour == "12":
            if meridian == "am":
                hour = "0"
        else:
            if meridian == "pm":
                hour = int(hour) + 12
                hour = str(hour)
        return hour

    def convertIconToBase64(self, iconStr):
        iconContent = convertSvgToPng( iconStr );
        pngBase64 = to_base64(iconContent)
        pngBase64 = base64_add_png_mimetype( pngBase64 )
        return pngBase64

    """
    Given a string of type WNW 10 mph it will split this string into two values.
    First value is the speed of the wind and the second value is the direction of the wind
    """
    def getWindSpeedAndDirection(self, windStr):
        windArr = windStr.split()
        return windArr[1], windArr[0]


    """
    Expect a string of the form: 79° (degree sign included) expressed in Fahrenheit.
    This method will convert it to Celsius and return it with the degree sign included
    """
    def convertToCelsius( self, temperatureStr ):
        #Last character is the degree sign, so remove it before making the conversion
        temperatureStr = temperatureStr[:-1]
        temperatureInt = int( temperatureStr )
        temperatureInt = int( convert_fahrenheit_to_celsius(temperatureInt) )
        temperatureStr = str( temperatureInt )
        return temperatureStr
