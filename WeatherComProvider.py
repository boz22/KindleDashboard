from WeatherDatapoint import WeatherDatapoint
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

    def getHourByHour(self) -> List:
        page = requests.get(self.hourByHourUrl)
        datapoints = self.getDatapoints( page.text )
        return datapoints

    def getDatapoints(self, htmlText):
        soup = BeautifulSoup(htmlText, 'html.parser')
        section = soup.find("section", attrs={ 'data-testid': 'HourlyForecast' });
        detailsSections = section.select("details");
        dpList = []
        for detailSection in detailsSections:
            #Summary card
            detailSummary = detailSection.find("summary")
            hour = detailSummary.find('h3', attrs={ 'data-testid': 'daypartName' })
            temperature = detailSummary.find('span', attrs={ 'data-testid': 'TemperatureValue' })
            iconAndSummary = detailSummary.find('div', attrs={ 'data-testid': 'wxIcon' })
            icon = iconAndSummary.find("svg");
            icon['xmlns:xlink'] = "http://www.w3.org/1999/xlink"
            icon = inlineSvg( icon, soup )
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

    def buildHourlyDatapoint(self, hour, temperature, icon, summary, precip, wind, humidity, uvIndex ):
        hourStr = hour.text
        temperatureStr = temperature.text
        temperatureStr = self.convertToCelsius( temperatureStr )
        iconStr = str(icon)
        iconStr = self.convertIconToBase64( iconStr )
        summaryStr = summary.text
        precipStr = precip.text
        windStr = wind.text
        windStr = self.convertToKilometers( windStr )
        humidityStr = humidity.text
        uvIndexStr = uvIndex.text
        datapoint = WeatherDatapoint( temperatureStr, iconStr, summaryStr, precipStr, windStr, humidityStr, uvIndexStr )
        return datapoint


    def convertIconToBase64(self, iconStr):
        iconContent = convertSvgToPng( iconStr );
        pngBase64 = to_base64(iconContent)
        pngBase64 = base64_add_png_mimetype( pngBase64 )
        return pngBase64

    """
    Receive a string of the form: WSW <x> mph.
    Will transform it into a string of the form: WSW <y> kmph.
    x - value in miles per hour
    y - value in kilometers per hour
    Formula is km = miles / 0.62137
    """
    def convertToKilometers( self, windStr ):
        windArr = windStr.split();
        milesStr = windArr[1]
        milesInt = int( milesStr )
        kmInt = int( convert_miles_to_km(milesInt) )
        windStr = windArr[0] + " " + str(kmInt) + " kmph"
        return windStr


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
        temperatureStr += degree_sign;
        return temperatureStr
