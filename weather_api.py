# import requests
# from flask import Flask, render_template, request, redirect, url_for
# from datetime import datetime
# from sqlalchemy import Column ,create_engine , String, ForeignKey, Date
#
# from sqlalchemy.orm import sessionmaker, Mapped
# import flask_wtf
# import wtforms
# from flask import request, Flask, render_template, url_for, redirect,session,jsonify
# from wtforms import StringField, SubmitField, IntegerField, PasswordField , DateField
# from sqlalchemy.orm import DeclarativeBase , sessionmaker, Mapped, mapped_column
# from wtforms.validators import InputRequired
#                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 api_key = "6ef4e7612bde555867a4a6aa9c2fe746"
#
# engine = create_engine('sqlite:///weather1.db', echo=True)
# Session = sessionmaker(bind=engine)
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = '07031986'
# weather = ['bez_hmarno.jpg','cold.jpg','Groza.jpg','hmarno.jpg','rain.jpg','Tuman.jpg','default.jpg','sun.jpg']
#
# class Base(DeclarativeBase):
#     def create_db(self):
#         Base.metadata.create_all(engine)
#
#     def drop_db(self):
#         Base.metadata.drop_all(engine)
# class City(flask_wtf.FlaskForm):
#     city = wtforms.StringField('Введіть місто', validators=[wtforms.validators.InputRequired()])
#     submit = wtforms.SubmitField('Goo!')
#
# class Submit(flask_wtf.FlaskForm):
#     submit = wtforms.SubmitField('Дізнатися погоду')
#
# class text(Base):
#     __tablename__ = "text"
#     id: Mapped[int] = mapped_column(primary_key=True)
#     text1: Mapped[int] = mapped_column(String(80))
#     user_id: Mapped[int] = mapped_column(ForeignKey('log.id'))
#
# @app.route('/')
# def f_1():
#     return render_template('host.html')
# @app.route('/weather_pg')
# def f_6():
#     return render_template('weather_pg1.html')
#
# # @app.route('/weather', methods = ['POST'])
# # def f_7():
# #     city = request.form['text']
# #     url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
# #     res = requests.get(url)
# #     if res.status_code == 200:
# #         data1 = res.json()
# #         session1 = session.get('list', [])
# #         if city not in session1:
# #             session1.append(city)
# #             session['list'] = session1
# #         weather_foto = weather[4]
# #         data = {'Тeмпература': f'{round(data1["main"]["temp"] - 273, 1)}',"Вологість" : f'{data1["main"]["humidity"]}', 'Швидкість вітру:' : f'{data1["wind"]["speed"]}','Картинка' : f'{weather_foto}'}
# #         print(data1)
# #     else:
# #         data = {'Тeмпература': f'Виникла помилка('}
# #     return jsonify(data), 200
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
#         temperature = round(data1["main"]["temp"] - 273, 1)
#         humidity = data1["main"]["humidity"]
#         wind_speed = data1["wind"]["speed"]
#
#         if temperature > 25:
#             weather_photo = "sun1.jfif"
#         elif 20 <= temperature <= 30:
#             weather_photo = "sun.jpg"
#         elif 10 <= temperature < 20:
#             weather_photo = "proholodno.jfif"
#         elif temperature < 10:
#             weather_photo = "cold.jpg"
#         data = {'Тeмпература': f'{round(data1["main"]["temp"] - 273, 1)}',"Вологість" : f'{data1["main"]["humidity"]}', 'Швидкість вітру:' : f'{data1["wind"]["speed"]}','Картинка' : f'{weather_photo}'}
#     else:
#         data = {'Тeмпература': f'Виникла помилка('}
#
#     return jsonify(data), 200
#
#
#
#
# @app.route('/weather_day')
# def get_weather():
#     return render_template('weather_5day.html')
#
# @app.route('/weather_map')
# def weather_map():
#     return render_template('weather_map.html')
# @app.route('/weather_5day', methods=['POST'])
# def get_weather_5day():
#     city = request.form['text']
#     url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric'
#     res = requests.get(url)
#
#     if res.status_code == 200:
#         data = res.json()
#         forecasts = []
#         daily_forecast = {}
#         for item in data['list']:
#             date, time = item['dt_txt'].split()
#             date = datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%Y')
#             if date not in daily_forecast:
#                 daily_forecast[date] = {'temperature': [], 'humidity': [], 'wind_speed': []}
#             daily_forecast[date]['temperature'].append(item['main']['temp'])
#             daily_forecast[date]['humidity'].append(item['main']['humidity'])
#             daily_forecast[date]['wind_speed'].append(item['wind']['speed'])
#
#         for date, values in daily_forecast.items():
#             forecast = {
#                 'date': date,
#                 'temperature': round(sum(values['temperature']) / len(values['temperature']), 1),
#                 'humidity': round(sum(values['humidity']) / len(values['humidity']), 1),
#                 'wind_speed': round(sum(values['wind_speed']) / len(values['wind_speed']), 1)
#             }
#             forecasts.append(forecast)
#
#         return jsonify({'forecast': forecasts}), 200
#     else:
#         return jsonify({'error': 'Failed to fetch weather forecast'}), 500
#
#
# # base =Base()
# # base.create_db()
#
# if __name__ == '__main__':
#     app.run(debug=True, port=8000)