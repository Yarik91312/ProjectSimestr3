from flask import Flask, request, session, jsonify, render_template
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import flask_wtf
import wtforms
from wtforms.validators import InputRequired
import requests
from datetime import datetime




app = Flask(__name__)


api_key = "6ef4e7612bde555867a4a6aa9c2fe746"
# База даних
engine = create_engine('sqlite:///app.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)




# Моделі
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

Base.metadata.create_all(engine)

# Форми
class City(flask_wtf.FlaskForm):
    city = wtforms.StringField('Введіть місто', validators=[InputRequired()])
    submit = wtforms.SubmitField('Goo!')

class Submit(flask_wtf.FlaskForm):
    submit = wtforms.SubmitField('Дізнатися погоду')

# Маршрути
@app.route('/')
def index():
    return render_template('index1.html')
@app.route('/host')
def f_1():
    return render_template('host.html')








@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        with Session() as session:
            user = User(username=username, email=email, password=password)
            session.add(user)
            session.commit()
        # msg = Message('Ласкаво просимо в наш додаток!', recipients=[email])
        # msg.body = f'Дякуємо за реєстрацію! Ваш логін: {username}, Ваш пароль: {password}'
        # mail.send(msg)
        return jsonify({'message': 'Користувач успішно зареєстрований'}), 200
    else:
        return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return jsonify({'message': 'Потрібно ввести ім`я користувача і пароль'}), 400
        session_db = Session()
        user = session_db.query(User).filter_by(username=username, password=password).first()
        if user:
            session['logged_in'] = True
            session_db.close()
            response = jsonify({'message': 'Вхід успішний', 'success': True})
            response.set_cookie('username', username)
            return response
        else:
            session_db.close()
            return jsonify({'message': 'Неправильне ім`я користувача або пароль', 'success': False}), 401
    else:
        return render_template('login.html')


@app.route('/weather', methods=['POST'])
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

        temperature = round(data1["main"]["temp"] - 273, 1)
        humidity = data1["main"]["humidity"]
        wind_speed = data1["wind"]["speed"]

        if temperature > 25:
            weather_photo = "very_hot.jpeg"
        elif 20 <= temperature <= 30:
            weather_photo = "sun2.jpeg"
        elif 10 <= temperature < 20:
            weather_photo = "cool.jpeg"
        elif temperature < 10:
            weather_photo = "very_cool.jpeg"
        data = {'Тeмпература': f'{round(data1["main"]["temp"] - 273, 1)}',"Вологість" : f'{data1["main"]["humidity"]}', 'Швидкість вітру:' : f'{data1["wind"]["speed"]}','Картинка' : f'{weather_photo}'}
    else:
        data = {'Тeмпература': f'Виникла помилка('}

    return jsonify(data), 200

@app.route('/weather_5day', methods=['POST'])
def get_weather_5day():
    city = request.form['text']
    api_key = "6ef4e7612bde555867a4a6aa9c2fe746"
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
            forecast = {
                'date': date,
                'temperature': round(sum(values['temperature']) / len(values['temperature']), 1),
                'humidity': round(sum(values['humidity']) / len(values['humidity']), 1),
                'wind_speed': round(sum(values['wind_speed']) / len(values['wind_speed']), 1)
            }
            forecasts.append(forecast)
        return jsonify({'forecast': forecasts}), 200
    else:
        return jsonify({'error': 'Failed to fetch weather forecast'}), 500

@app.route('/weather_pg')
def weather_pg():
    return render_template('weather_pg1.html')

@app.route('/weather_map')
def weather_map():
    return render_template('weather_map.html')

@app.route('/weather_day')
def weather_day():
    return render_template('weather_5day.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
