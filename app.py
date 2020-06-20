from flask import Flask
from flask import render_template
from WeatherComProvider import WeatherComProvider
from data_utils import objects_list_to_csv
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from images_utils import base64_add_png_mimetype
from images_utils import to_base64

app = Flask(__name__)

@app.route('/status')
def status():
    return "Running !"

@app.route('/weather/now')
def weather_now():
    weatherCom = WeatherComProvider()
    #Get forecast for next days
    nextDays = weatherCom.getDaily();
    today = nextDays[0]
    nextDays = nextDays[1:3]

    #Hour by hour and build graph with precipitation
    dpList = weatherCom.getHourByHour();
    csv = objects_list_to_csv( dpList )
    data = StringIO( csv )
    df = pd.read_csv(data)
    df = df[:24]
    df = df.filter(['hour', 'precip'], axis=1)

    #Font Size. THis updates the font size of all elements
    plt.rcParams.update({'font.size': 18})

    #Plot the graph. Width=1 will have the effect of no whitespace between bars
    # rot=0 makes the x ticks display horizonally
    ax = df.plot(x='hour', kind='bar', width=1, figsize=(10,5), rot=0);
    plt.yticks([0, 30, 50, 70, 100], ['0%', '30%', '50%', '70%', '100%'])
    xlocs, xlabels = plt.xticks();
    k=0
    #Display xticks. Will make the hour display with ':00' but only display hours at interval of 2 hours.
    #e.g.: 14:00, 16:00. This is to save space
    for label in xlabels:
        if k % 2 == 0:
            crtLabel = label.get_text()
            crtLabel = crtLabel + ":00"
            label.set_text( crtLabel )
        else:
            label.set_text( "" )
        k = k +1
    plt.xticks(xlocs, xlabels)

    #Remove whitespaces and values on the y axis, leave only the X axis to show hours
    plt.subplots_adjust(top = 1, bottom = 0.2, right = 1, left = 0, hspace = 0, wspace = 0)

    #Put values of the y-axis directly on the bar chart values.
    y = df['precip']
    k=0
    for p in ax.patches:
        if k % 2 == 0:
            ax.annotate(str(p.get_height()) + "%", (p.get_x() * 1.000, p.get_height() * 1.005))
        k=k+1


    plt.savefig('/tmp/precip.png')
    f = open("/tmp/precip.png", "rb")
    pngContent = f.read();
    f.close()
    pngBase64 = to_base64(pngContent)
    pngBase64 = base64_add_png_mimetype( pngBase64 )
    return render_template('weather.html', precipImageSrc=pngBase64, nextDays=nextDays, today=today, nextHour=dpList[0])


if __name__ == '__main__':
    app.run(host='0.0.0.0')
