#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import json
import socketserver
from time import gmtime, strftime, time

usage_error = 'usage: python3 server.py <port>'


class SIPRegistrerHandler(socketserver.DatagramRequestHandler):

    dicc = {}

    def register2json(self):
        with open('registered.json', 'w') as jsonfile:
            json.dump(self.dicc, jsonfile, indent=3)

    def json2registered(self):
        try:
            with open('registered.json', 'r') as jsonfile:
                self.dicc = json.load(jsonfile)
                self.expiration()
        except(FileNotFoundError):
            pass

    def expiration(self):
        expired = []
        time_exp = strftime('%Y-%m-%d %H:%M:%S', gmtime(time()))
        for user in self.dicc:
            if self.dicc[user][1] <= time_exp:
                expired.append(user)
        for user in expired:
            del self.dicc[user]

    def handle(self):
        self.json2registered()
        data = self.rfile.read().decode('utf-8')
        if 'REGISTER' in data:
            username = data.split('\r\n')[0].split()[2]
            exp_time = int(data.split('\r\n')[1].split()[1])
            expires = exp_time + time()
            expires_str = strftime('%Y-%m-%d %H:%M:%S', gmtime(expires))
            if username in self.dicc:
                if exp_time != 0:
                    self.dicc[username] = [self.client_address[0], expires_str]
                    print('user update')
                    self.wfile.write(b'SIP/2.0 200 OK\r\n')
                else:
                    try:
                        del self.dicc[username]
                        self.wfile.write(b'SIP/2.0 200 OK\r\n')
                    except:
                        self.wfile.write(b'SIP/2.0 404 User Not Found\r\n')
            else:
                self.dicc[username] = [self.client_address[0], expires_str]
                self.wfile.write(b'SIP/2.0 200 OK\r\n')
        self.register2json()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(usage_error)
    else:
        port = sys.argv[1]
    serv = socketserver.UDPServer(('', int(port)), SIPRegistrerHandler)

    print('Lanzando servidor UDP de eco...')
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print('Finalizado servidor')
