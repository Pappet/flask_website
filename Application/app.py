from blueprints.main.main import main_blueprint
from datetime import datetime
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from models import User, Message
from extensions import db, bcrypt

import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
# You can use other database systems like PostgreSQL or MySQL
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///postgres:POSTnP145A18@192.168.178.37/flask_website'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)

# Importieren und Registrieren des Blueprints
app.register_blueprint(main_blueprint)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.login'


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(401)
def page_not_found(e):
    return render_template('401.html'), 401


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@socketio.on('send_message')
def handle_send_message(message):
    # Füge den Benutzernamen zur Nachricht hinzu
    message["username"] = current_user.username
    # Füge die aktuelle Uhrzeit zur Nachricht hinzu
    message["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Erstelle ein neues Message-Objekt und speichere es in der Datenbank
    new_message = Message(username=message["username"], content=message["message"],
                          timestamp=datetime.strptime(message["time"], "%Y-%m-%d %H:%M:%S"))
    db.session.add(new_message)
    db.session.commit()

    socketio.emit('recive_message', message)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
