from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, session, request, make_response
from flask_socketio import SocketIO, emit, join_room, leave_room, disconnect

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'chatworld'
socketio = SocketIO(app)

users = {}

@app.route('/', methods=['GET', 'POST'])
def chat():
    global users
    # if request.method == 'POST':
    #     print("post")
    #     users = users.update(request.get_json(force=True))
    #     success = ""
        # return make_response(success)
    if request.method == 'GET':
        print(users)
        return render_template('chat.html')

@app.route('/login')
def login():
    return render_template('login.html')

@socketio.on('message', namespace='/chat')
def chat_message(message):
    print("message = ", message)
    emit('message', {'data': message['data']}, broadcast=True)

@socketio.on('connect', namespace='/chat')
def test_connect():
    foo = request.args.get('author')
    print(foo)
    emit('my response', {'data': 'Connected', 'count': 0})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
