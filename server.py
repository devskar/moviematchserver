import eventlet
from eventlet import wsgi
import socketio

from objects.game import Game

server = socketio.Server()
app = socketio.WSGIApp(server)

game = Game()


# SERVER EVENTS
@server.event
def connect(sid, environ):
    print(f'[CLIENT] {sid} connected')


@server.event
def disconnect(sid):
    leave_room(sid)
    print(f'[CLIENT] {sid} disconnected')


@server.event
def register(sid, name):
    game.register_user(sid, name)
    print(f'[NEW PLAYER] {name} registered')


# ROOM EVENTS
@server.event
def create_room(sid):
    if not game.find_room_by_user(sid):
        room = game.create_room(game.find_user_by_sid(sid))
        print(f'[ROOM] {game.find_user_by_sid(sid).name} created room {room.id}')

        join_room(sid, room.id)
        return room


@server.event
def join_room(sid, room_id):
    room = game.find_room_by_id(room_id)
    user = game.find_user_by_sid(sid)

    if room:
        room.add_user(user)
        server.enter_room(sid, room_id)
        print(f'[ROOM] {game.find_user_by_sid(sid).name} joined room {room_id}')

        server.emit('new_member', data=user.name, room=room.id, skip_sid=sid)


@server.event
def leave_room(sid):
    room = game.find_room_by_user(game.find_user_by_sid(sid))

    if room:
        server.leave_room(sid, room.id)
        room.remove_user(game.find_user_by_sid(sid))

        print(f'[ROOM] {game.find_user_by_sid(sid).name} left room {room.id}')


@server.event
def get_room_member(sid):
    return [user.name for user in game.find_room_by_user(sid).participants]


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app, log_output=False)
