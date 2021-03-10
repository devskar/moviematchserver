import eventlet
from eventlet import wsgi
import socketio

from objects.responses import Response
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

    return Response.SUCCESS.value


# ROOM EVENTS
@server.event
def create_room(sid, name):
    if not game.find_room_by_user(sid):
        room = game.create_room(name)
        print(f'[ROOM] {game.find_user_by_sid(sid).name} created room  {room.name}({room.id})')

        join_room(sid, room.id)
        return Response.SUCCESS.value
    else:
        return Response.FAILURE.value


@server.event
def join_room(sid, room_id):
    room = game.find_room_by_id(room_id)
    user = game.find_user_by_sid(sid)

    if room:
        room.add_user(user)
        server.enter_room(sid, room=room.id)

        print(f'[ROOM] {game.find_user_by_sid(sid).name} joined room  {room.name}({room.id})')

        server.emit('member_join', data=user.name, room=room.id, skip_sid=sid)

        return Response.SUCCESS.value
    return Response.FAILURE.value


@server.event
def leave_room(sid):
    room = game.find_room_by_user(sid)
    user = game.find_user_by_sid(sid)

    if room:
        room.remove_user(user)  # removes user from the game room
        server.leave_room(sid, room=room.id)  # removes user from the server room

        print(f'[ROOM] {game.find_user_by_sid(sid).name} left room {room.name}({room.id})')

        server.emit('member_leave', data=user.name, room=room.id, skip_sid=sid)
        return Response.SUCCESS.value
    return Response.FAILURE.value


@server.event
def get_room_info(sid):
    room = game.find_room_by_user(sid)

    if not room:
        return Response.FAILURE.value

    return room.id, room.name


@server.event
def get_room_movie(sid):
    room = game.find_room_by_user(sid)

    if not room:
        return Response.FAILURE.value

    return room.current_movie


@server.event
def get_room_member(sid):
    return [user.name for user in game.find_room_by_user(sid).participants]


@server.event
def match_movie(sid):
    player = game.find_user_by_sid(sid)
    room = game.find_room_by_user(sid)

    print(player.name, 'matches movie: ', room.current_movie['title'])


@server.event
def nomatch_movie(sid):
    player = game.find_user_by_sid(sid)
    room = game.find_room_by_user(sid)

    print(player.name, 'doesn\'t matches movie: ', room.current_movie['title'])


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app, log_output=False)
