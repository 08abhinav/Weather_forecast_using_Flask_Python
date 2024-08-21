from flask import Flask, render_template, request
import requests
from flask_bootstrap import Bootstrap5
import math
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
Bootstrap5(app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///weather.db"
db = SQLAlchemy()
db.init_app(app)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = Weather(name=new_city)

            db.session.add(new_city_obj)
            db.session.commit()

    cities = Weather.query.all()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&APPID="ADD YOUR APPID"'
    weather_data = []
    for city in cities:
        r = requests.get(url.format(city.name)).json()
        weather = {
            'city': city.name,
            'icon': r['weather'][0]['icon'],
            'temperature_in_celsius': math.floor(r['main']['temp']-273.15),
            'temperature_in_fahrenheit': math.floor(((r['main']['temp']-273.15)*1.8)+32),
            'description': r['weather'][0]['description'].title(),
            'temp_min': math.floor(r['main']['temp_min']-273.15),
            'temp_max': math.floor(r['main']['temp_max']-273.15),
            'feels_like': math.floor(r['main']['feels_like']-273.15),
            'humidity': r['main']['humidity'],
            'visibility': (r['visibility'])/1000,
            'wind': r['wind']['speed'],
            'sunrise': r['sys']['sunrise'],
            'sunset': r['sys']['sunset']
        }
        weather_data.append(weather)

    return render_template('home.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=True)
