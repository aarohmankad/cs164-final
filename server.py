import json
import socket

from inspect import cleandoc
from thread import *

HOST = ''
PORT = 5000
clients = {
  'aaroh': {
    'password': 'subway',
    'isOnline': False,
    'connection': None,
    'queue': [],
  },
  'patrick': {
    'password': 'shiba',
    'isOnline': False,
    'connection': None,
    'queue': [],
  }
}

def client_thread(c):
  try:
    c.send('Welcome! Please log in.\n')
    c.send('Username: ')
    username = c.recv(1024)
    c.send('Password: ')
    password = c.recv(1024)

    if username not in clients or clients[username]['password'] != password:
      c.send('Invalid Username/Password combination.\n')
      c.close()

    clients[username]['isOnline'] = True;
    clients[username]['connection'] = c;

    menu = cleandoc("""
    MENU
    ================
    [1] Logout
    [2] Change Password
    [3] Send Message
    [4] List Unread Messages
    [5] Broadcast To All Online Users
    """)
    c.send(menu + "\n\n")
    c.send('You have {} unread messages\n\n'.format(len(clients[username]['queue'])))

    while 1:
      data = c.recv(1024)
      if not data:
          c.send('I didn\'t get that. Try again.')
          continue

      if data == '1':
        clients[username]['isOnline'] = False;
        c.send('Goodbye.\n')
        c.close()
      if data == '2':
        c.send('Old Password: ')
        old_password = c.recv(1024)
        c.send('New Password: ')
        new_password = c.recv(1024)

        if old_password == clients[username]['password']:
          clients[username]['password'] = new_password
          c.send('You have successfully changed your password.\n')
        else:
          c.send('Sorry, something went wrong.')
      if data == '3':
        c.send('To: ')
        receiver = c.recv(1024)
        c.send('Message: ')
        message = c.recv(1024)

        if clients[receiver]['isOnline']:
          c.send('Sent Message!\n\n')
          clients[receiver]['connection'].send('{}: {}'.format(username, message))
          clients[receiver]['connection'].send(menu)
        else:
          c.send('They\'re not online right now. They will receive your message when they log back in\n\n')
          clients[receiver]['queue'].append({'from': username, 'message': message})
      if data == '4':
        for message in clients[username]['queue']:
          c.send('{}: {}'.format(message['from'], message['message']))

        del clients[username]['queue'][:]
      if data == '5':
        c.send('Message: ')
        message = c.recv(1024)
        for clientname in clients:
          if clients[clientname]['isOnline']:
            clients[clientname]['connection'].send('{}: {}'.format(username, message))
            clients[clientname]['connection'].send(menu)

        c.send('Broadcasted Message!')
      c.send('\n\n' + menu + "\n\n")
  except:
    print('Client disconnected')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)
print('Waiting on incoming connections to localhost:{}'.format(PORT))

while 1:
  connection, address = s.accept()
  print('Connected with {}:{}'.format(address[0], address[1]))
  start_new_thread(client_thread, (connection,))

s.close()
