from __future__ import print_function

import getpass
import json
import socket

from threading import Timer

HOST = ''
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def login():
    user = raw_input("Username [%s]: " % getpass.getuser())
    if not user:
        user = getpass.getuser()

    pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))

    password, confirm_password = pprompt()
    while password != confirm_password:
        print('Passwords do not match. Try again')
        password, confirm_password = pprompt()

    return user, password

while 1:
  prompt, address = s.recvfrom(1024)
  print(prompt, end='')

  if prompt == 'Goodbye.\n':
    break;

  reply = ''
  if 'Password' in prompt and 'MENU' not in prompt:
    reply = getpass.getpass('')
  else:
    reply = raw_input()
  
  s.send(reply)

s.close()
