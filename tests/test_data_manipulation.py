import sys
sys.path.append('../')
import unittest
from data_utils import objects_list_to_csv;
from WeatherDatapoint import WeatherDatapoint

class TestDataManipulatoin( unittest.TestCase ):

    def testListToCsv(self):
        print('Running testListToCsv')
        datapoint1 = WeatherDatapoint( "8 am", "31", "icon1", "Cloudy", "31%", "31kmh", "21", "2" )
        datapoint2 = WeatherDatapoint( "9 am", "33", "icon2", "Cloudy", "31%", "37kmh", "25", "3" )
        datapoint3 = WeatherDatapoint( "10 am", "35", "icon3", "Sunny", "31%", "38kmh", "26", "1" )
        dps = [];
        dps.append(datapoint1);
        dps.append(datapoint2);
        dps.append(datapoint3);
        csv = objects_list_to_csv( dps )
        print(csv)
        startsOk = csv.startswith("hour,humidity")
        self.assertEqual(True, startsOk)

    def testEmptyListToCsv(self):
        print('Running testEmptyListToCsv')
        dps = [];
        csv = objects_list_to_csv( dps )
        self.assertEqual("", csv)

if __name__ == '__main__':
    unittest.main()
