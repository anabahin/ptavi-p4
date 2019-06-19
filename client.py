#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import socket

ussage_error = 'usage: python3 client.py <ip><port><method><username><expires>'

if len(sys.argv) < 6:
    sys.exit(usage_error)

server_ip = sys.argv[1]
server_port = sys.argv[2]
method = sys.argv[3]
username = sys.argv[4]
expires = sys.argv[5]

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((server_ip, int(server_port)))
    print('Enviando:', method.upper())
    if method.upper() == 'REGISTER':
        mess = method.upper() + ' sip: ' + username + ' SIP/2.0\r\nExpires: '
        mess += expires + '\r\n'
        my_socket.send(bytes(mess, 'utf-8') + b'\r\n')
        data = my_socket.recv(1024).decode('utf-8')
        if data:
            print('Recibido -- ', data)
        else:
            print('No server listening at', server_ip + ':' + server_port)

print('Socket terminado.')
