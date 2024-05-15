from flask import Flask, request, session, jsonify, render_template, redirect, url_for, make_response
from sqlalchemy import create_engine, Column, String, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_mail import Mail, Message
from config import MAIL, MAIL_PASSWORD

app = Flask(__name__)
app.secret_key = '203965'

engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)


Base.metadata.create_all(engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = '12212112'
app.config['MAIL_SERVER'] = 'smtp.ukr.net'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = MAIL
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_DEFAULT_SENDER'] = MAIL
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



@app.route('/')
def index():
    return render_template('index1.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user = User(username=username, email=email, password=password)
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(user)
        session.commit()
        msg = Message('Ласкаво просимо в наш додаток!', recipients=[email])
        msg.body = f'Дякуємо за реєстрацію! Ваш логін: {username}, Ваш пароль: {password}'
        mail.send(msg)

        return jsonify({'message': 'Користувач успішно зареєстрований'})
    else:
        return render_template('signup.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return jsonify({'message': 'Потрібно ввести ім`я користувача і пароль'}), 400

        Session = sessionmaker(bind=engine)
        db_session = Session()
        user = db_session.query(User).filter_by(username=username, password=password).first()

        if user:
            session['logged_in'] = True
            db_session.close()

            response = jsonify({'message': 'Вхід успішний'})
            response.set_cookie('username', username)
            return response
        else:
            db_session.close()
            return jsonify({'message': 'Неправильне ім`я користувача або пароль'}), 401
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)

