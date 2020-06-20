import sys
sys.path.append('../')
import unittest
from data_utils import objects_list_to_csv;
from WeatherDatapoint import WeatherDatapoint
import pandas as pd
import matplotlib.pyplot as plt

class TestDataManipulatoin( unittest.TestCase ):

    def testListToCsv(self):
        print('Running testListToCsv')
        datapoint1 = WeatherDatapoint( "8 am", "31", "icon1", "Cloudy", "31%", "31kmh", "NWN", "21", "2" )
        datapoint2 = WeatherDatapoint( "9 am", "33", "icon2", "Cloudy", "31%", "37kmh", "NWN", "25", "3" )
        datapoint3 = WeatherDatapoint( "10 am", "35", "icon3", "Sunny", "31%", "38kmh", "NWN", "26", "1" )
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


    def testPlotGeneration(self):
        df = pd.read_csv("datapoints.csv")
        df = df[:24]
        df = df.filter(['hour', 'precip'], axis=1)
        df.plot(x='hour', kind='bar');
        plt.yticks([0, 30, 50, 70, 100], ['0%', '30%', '50%', '70%', '100%'])
        xlocs, xlabels = plt.xticks();
        #print(xlocs)
        for label in xlabels:
            crtLabel = label.get_text()
            crtLabel = crtLabel + ":00"
            label.set_text( crtLabel )
        plt.xticks(xlocs, xlabels)

        plt.savefig('foo.png')


if __name__ == '__main__':
    unittest.main()
