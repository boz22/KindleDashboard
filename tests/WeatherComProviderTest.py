import sys
sys.path.append('../')
import unittest
from unittest import mock
from weather_utils import degree_sign

from WeatherComProvider import WeatherComProvider

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self):
            f = open("hour_by_hour.html", "r")
            self.text = f.read()
            f.close()
    return MockResponse()


class WeatherComProviderTest( unittest.TestCase ):
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testHourByHour(self, mock_get):
        weatherCom = WeatherComProvider()
        dpList = weatherCom.getHourByHour();
        self.assertEqual( '26' + degree_sign, dpList[0].temperature )
        self.assertEqual( 48, len(dpList) )
        startsWithTest = dpList[2].icon.startswith("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMgAAADICAYAAACtWK6eA")
        self.assertTrue( startsWithTest )

if __name__ == '__main__':
    unittest.main()
