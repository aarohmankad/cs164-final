import json
import socket

from inspect import cleandoc
from thread import *

HOST = ''
PORT = 5000
clients = {
  'aaroh': {
    'password': 'password',
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
      c.send('Invalid Username/Password combination.')

    menu = cleandoc("""
    MENU
    ================
    [1] Logout
    [2] Change Password
    """)
    c.send(menu + "\n\n")

    while 1:
      data = c.recv(1024)
      if not data:
          c.send('I didn\'t get that. Try again.')
          continue

      if data == '1':
        c.send('Goodbye.\n')
        c.close()
      if data == '2':
        c.send('Old Password: ')
        old_password = c.recv(1024)
        c.send('New Password: ')
        new_password = c.recv(1024)

        if old_password == clients[username]['password']:
          clients[username]['password'] = new_password
          c.send('You have successfully changed your password.')
        else:
          c.send('Sorry, something went wrong.')

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
