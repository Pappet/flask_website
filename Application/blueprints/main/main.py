# blueprints/main.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, abort, jsonify
from flask_login import login_user, login_required, logout_user
from extensions import db, bcrypt
from models import User, Message

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
@login_required
def index():
    return render_template('index.html')


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('main.index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('main.login'))
    return render_template('register.html')


@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))


@main_blueprint.route('/logged_in_user')
def logged_in_user():
    from flask_login import current_user
    if current_user.is_authenticated:
        return str(current_user.username)  # Convert the integer to a string
    else:
        abort(401)  # Unauthorized


@main_blueprint.route('/get_messages')
@login_required
def get_messages():
    messages = Message.query.order_by(Message.timestamp).all()
    messages_json = []
    for message in messages:
        messages_json.append({
            "username": message.username,
            "message": message.content,
            "time": message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(messages_json)
