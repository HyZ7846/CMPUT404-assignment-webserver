#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.data = self.data.decode('utf-8')
        #print("Got a request of: %s\n" % self.data)
        if self.data.split(" ")[0] == 'GET':
            req_file = self.data.split(" ")[1] # /index.html
            
            if req_file == '/':# handle empty directory
                req_file = '/index.html'
            
            
            if '..' in req_file:# handle home directory
                self.request.sendall(bytearray(f'HTTP/1.0 404 NOT FOUND\r\n\n', 'utf-8'))
            
            
            try:
                with open('www%s' % req_file,'r') as open_file:
                    file_content = open_file.read()
                    file_type = req_file.split(".")[1]
                    if file_type != '': # html
                        self.request.sendall(bytearray(f'HTTP/1.0 200 OK\r\nContent-Type: text/{file_type}\r\n\n{file_content}', 'utf-8'))
            
            
            except FileNotFoundError as fileNotFound: # handle file not found 404
                #print(fileNotFound)
                self.request.sendall(bytearray(f'HTTP/1.0 404 NOT FOUND\r\n\n', 'utf-8'))
                
                
            except IsADirectoryError as isADirectory:
                #print(isADirectory)
                if req_file[-1] == '/': # handle request deep/
                    req_file += 'index.html'
                    with open('www%s' % req_file,'r') as open_file:
                        file_content = open_file.read()
                        file_type = req_file.split(".")[1]
                    self.request.sendall(bytearray(f'HTTP/1.0 200 OK\r\nContent-Type: text/{file_type}\r\n\n{file_content}', 'utf-8'))
                    
                else: # handle request deep
                    req_file += '/index.html'
                    with open('www%s' % req_file,'r') as open_file:
                        file_content = open_file.read()
                        file_type = req_file.split(".")[1]
                    self.request.sendall(bytearray(f'HTTP/1.0 301 The URL has been moved permanently\r\nContent-Type: text/{file_type}\r\n\n{file_content}', 'utf-8'))
                    
                    
        else: # handle other method: POST/PUT other than GET
            self.request.sendall(bytearray(f'HTTP/1.0 405 Method Not Allowed\r\n\n', 'utf-8'))
            
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
