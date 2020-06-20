import sys
sys.path.append('../')
import unittest
from unittest import mock
from weather_utils import degree_sign
from data_utils import objects_list_to_csv;

from WeatherComProvider import WeatherComProvider

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, forecastType):
            if "hourbyhour" in forecastType:
                f = open("hour_by_hour.html", "r")
            else:
                f = open("daily.html", "r")
            self.text = f.read()
            f.close()

    forecastType = ""
    for arg in args:
        forecastType = arg
        break
    return MockResponse( forecastType )


class WeatherComProviderTest( unittest.TestCase ):
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testHourByHour(self, mock_get):
        weatherCom = WeatherComProvider()
        dpList = weatherCom.getHourByHour();
        self.assertEqual( '26', dpList[0].temperature )
        self.assertEqual( 48, len(dpList) )
        self.assertEqual("17", dpList[5].hour)
        self.assertEqual("0", dpList[12].hour)
        print(dpList[5].humidity)
        self.assertEqual("55", dpList[5].humidity)
        print(dpList[5].uvIndex)
        self.assertEqual("3", dpList[5].uvIndex)
        print(dpList[5].windSpeed)
        self.assertEqual("9", dpList[5].windSpeed)
        print(dpList[5].windDirection)
        self.assertEqual("WNW", dpList[5].windDirection)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testDaily(self, mock_get_daily):
        weatherCom = WeatherComProvider()
        dpList = weatherCom.getDaily();
        self.assertEqual(5, len( dpList ))


if __name__ == '__main__':
    unittest.main()
