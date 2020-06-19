from flask import Flask
from flask import render_template
from WeatherComProvider import WeatherComProvider

app = Flask(__name__)

@app.route('/status')
def status():
    return "Running !"

@app.route('/weather/now')
def weather_now():
    weatherCom = WeatherComProvider()
    dpList = weatherCom.getHourByHour();
    return render_template('weather.html', datapoints=dpList)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
