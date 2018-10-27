#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente UDP que abre un socket a un servidor
"""

import socket
import sys

# Constantes. Dirección IP del servidor y contenido a enviar
#paso la IP y puerto y el comentario
if len(sys.argv)<5:
    sys.exit("Usage: python3 client.py <ip> <port> <register> <sip_address> <expires_value>")

SERVER = sys.argv[1]
PORT = sys.argv[2]
COMMENT =(sys.argv[4])
EXPIRE = sys.argv[5]
            
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
    my_socket.connect((SERVER, int(PORT)))
    print("Enviando:", COMMENT)
    if sys.argv[3] == 'register':
        my_socket.send(bytes('REGISTER sip: '+COMMENT+'  SIP/2.0\r\nExpires: ' +EXPIRE+'\r\n\r\n','utf-8') + b'\r\n')
        data = my_socket.recv(1024)
    print('Recibido -- ', data.decode('utf-8'))

print("Socket terminado.")
