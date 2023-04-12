from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('send_message')
def handle_send_message(message):
    print('received message:', message)
    socketio.emit('message', message)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
