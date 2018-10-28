#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
from time import gmtime, strftime, time
import json

try:
    PORT = sys.argv[1]
except IndexError:
    sys.exit("Usage: python3 server.py <port>")


class SIPRegistrerHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    dic = {}
    
    def register2json(self):
        json.dump(self.dic, open('registered,json', 'w'))


    def json2registered(self):
        try:
            with open('registered.json', 'r') as file:
                self.dic = json.load(file)
                self.expiration()
        except:
            pass
    def expiration(self):
        expired = []
        time_exp = strftime('%Y-%m-%d %H:%M:%S', gmtime(time()))
        for user in self.dic:
            if self.dic[user][1] <= time_exp:
                expired.append(user)
        for user in expired:
            del self.dic[user]
    
    def handle(self):
        self.expiration()
        self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        print(self.client_address)
        for line in self.rfile:
            if line:
                if line.decode('utf-8')[:8] == 'REGISTER':
                    user = line.decode('utf-8')[13:-10]
                    ip = self.client_address[0]
                elif line.decode('utf-8')[:7] == 'Expires':
                    expires = int(line.decode('utf-8')[9:]) + time()
                    expire = strftime('%Y-%m-%d %H:%M:%S', gmtime(expires))
                    if line.decode('utf-8').split(' ')[1][0] != '0':
                        self.dic[user] = [ip, expire]
                    else:
                        del self.dic[user]
            print(line.decode('utf-8'),end='')
        print(self.dic)
        self.register2json()

if __name__ == "__main__":
    # Listens at localhost ('') port 6001 
    # and calls the EchoHandler class to manage the request
    serv = socketserver.UDPServer(('', int(PORT)), SIPRegistrerHandler) 

    print("Lanzando servidor UDP de eco...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
