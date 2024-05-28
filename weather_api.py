import requests
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from sqlalchemy import Column ,create_engine , String, ForeignKey, Date

from sqlalchemy.orm import sessionmaker, Mapped
import flask_wtf
import wtforms
from flask import request, Flask, render_template, url_for, redirect,session,jsonify
from wtforms import StringField, SubmitField, IntegerField, PasswordField , DateField
from sqlalchemy.orm import DeclarativeBase , sessionmaker, Mapped, mapped_column
from wtforms.validators import InputRequired
api_key = "6ef4e7612bde555867a4a6aa9c2fe746"

engine = create_engine('sqlite:///weather1.db', echo=True)
Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = '07031986'
weather = ['bez_hmarno.jpg','cold.jpg','Groza.jpg','hmarno.jpg','rain.jpg','Tuman.jpg','default.jpg','sun.jpg']

class Base(DeclarativeBase):
    def create_db(self):
        Base.metadata.create_all(engine)

    def drop_db(self):
        Base.metadata.drop_all(engine)
class City(flask_wtf.FlaskForm):
    city = wtforms.StringField('Введіть місто', validators=[wtforms.validators.InputRequired()])
    submit = wtforms.SubmitField('Goo!')

class Submit(flask_wtf.FlaskForm):
    submit = wtforms.SubmitField('Дізнатися погоду')

class text(Base):
    __tablename__ = "text"
    id: Mapped[int] = mapped_column(primary_key=True)
    text1: Mapped[int] = mapped_column(String(80))
    user_id: Mapped[int] = mapped_column(ForeignKey('log.id'))

@app.route('/')
def f_1():
    return render_template('host.html')
@app.route('/weather_pg')
def f_6():
    return render_template('weather_pg1.html')

@app.route('/weather', methods = ['POST'])
def f_7():
    city = request.form['text']
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
    res = requests.get(url)
    if res.status_code == 200:
        data1 = res.json()
        session1 = session.get('list', [])
        if city not in session1:
            session1.append(city)
            session['list'] = session1
        temperature = round(data1["main"]["temp"] - 273.15, 1)
        humidity = data1["main"]["humidity"]
        wind_speed = data1["wind"]["speed"]

        if temperature > 25:
            weather_photo = "very_hot.jpeg"
        elif 18 <= temperature <= 25:
            weather_photo = "sun2.jpeg"
        elif 10 <= temperature < 17:
            weather_photo = "cool.jpeg"
        elif temperature < 10:
            weather_photo = "very_cool.jpeg"
        elif 85 <= humidity <= 100:
            weather_photo = "rain.jpeg"

        data = {
            'Тeмпература': f'{temperature}',
            'Вологість': f'{humidity}',
            'Швидкість вітру:': f'{wind_speed}',
            'Картинка': weather_photo
        }

    else:
        data = {'Картинка': 'error.jpeg'}

    return jsonify(data), 200
# @app.route('/weather', methods=['POST'])
# def f_7():
#     city = request.form['text']
#     url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
#     res = requests.get(url)
#
#     if res.status_code == 200:
#         data1 = res.json()
#         session1 = session.get('list', [])
#         if city not in session1:
#             session1.append(city)
#             session['list'] = session1
#
#         temperature = round(data1["main"]["temp"] - 273.15, 1)
#         humidity = data1["main"]["humidity"]
#         wind_speed = data1["wind"]["speed"]
#
#         if temperature > 25:
#             weather_photo = "very_hot.jpeg"
#         elif 20 <= temperature <= 25:
#             weather_photo = "sun2.jpg"
#         elif 10 <= temperature < 20:
#             weather_photo = "cool.jpeg"
#         else:
#             weather_photo = "very_cool.jpeg"
#
#         data = {
#             'Тeмпература': f'{temperature}',
#             'Вологість': f'{humidity}',
#             'Швидкість вітру:': f'{wind_speed}',
#             'Картинка': weather_photo
#         }
#
#     else:
#         data = {'Картинка': 'error.jpeg'}
#
#     return jsonify(data), 200




@app.route('/weather_day')
def get_weather():
    return render_template('weather_5day.html')

@app.route('/weather_map')
def weather_map():
    return render_template('weather_map.html')
@app.route('/weather_5day', methods=['POST'])
def get_weather_5day():
    city = request.form['text']
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        forecasts = []
        daily_forecast = {}
        for item in data['list']:
            date, time = item['dt_txt'].split()
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y')
            if date not in daily_forecast:
                daily_forecast[date] = {'temperature': [], 'humidity': [], 'wind_speed': []}
            daily_forecast[date]['temperature'].append(item['main']['temp'])
            daily_forecast[date]['humidity'].append(item['main']['humidity'])
            daily_forecast[date]['wind_speed'].append(item['wind']['speed'])

        for date, values in daily_forecast.items():
            avg_temp = round(sum(values['temperature']) / len(values['temperature']), 1)
            avg_humidity = round(sum(values['humidity']) / len(values['humidity']), 1)
            avg_wind_speed = round(sum(values['wind_speed']) / len(values['wind_speed']), 1)

            weather_photo = ""

            if avg_temp > 25:
                weather_photo = "very_hot.jpeg"
            elif 18 <= avg_temp <= 25:
                weather_photo = "sun2.jpeg"
            elif 10 <= avg_temp < 18:
                weather_photo = "cool.jpeg"
            elif avg_temp < 10:
                weather_photo = "very_cool.jpeg"

            if avg_humidity >= 80:
                weather_photo = "rain.jpg"

            forecast = {
                'date': date,
                'temperature': avg_temp,
                'humidity': avg_humidity,
                'wind_speed': avg_wind_speed,
                'weather_photo': weather_photo
            }
            forecasts.append(forecast)

        return jsonify({'forecast': forecasts}), 200
    else:
        return jsonify({'error': 'Failed to fetch weather forecast'}), 500


# base =Base()
# base.create_db()

if __name__ == '__main__':
    app.run(debug=True, port=8000)