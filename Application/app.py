import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
# You can use other database systems like PostgreSQL or MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postgres:POSTnP145A18@192.168.178.37/flask_website'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
socketio = SocketIO(app)
login_manager.login_view = 'login'


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(id=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        user = User(id=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/logged_in_user')
def logged_in_user():
    if current_user.is_authenticated:
        return current_user.id
    else:
        return '', 401  # Unauthorized


@socketio.on('send_message')
def handle_send_message(message):
    # Füge den Benutzernamen zur Nachricht hinzu
    message["username"] = current_user.id
    # Füge die aktuelle Uhrzeit zur Nachricht hinzu
    message["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(message)
    socketio.emit('recive_message', message)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.String(80), primary_key=True)
    password = db.Column(db.String(80), nullable=False)
