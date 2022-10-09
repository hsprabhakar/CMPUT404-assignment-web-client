#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
#       http://127.0.0.1:8080/
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

# Author: Harish Prabhakar
# University of Alberta
# Instructor: Campbell Hazel
# CMPUT404 F2022

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse
TEST_SERVER = "127.0.0.1"
def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        # print('iNITIAL SOCKET   ', self.socket, "\n\n\n")

        return None

    def get_code(self, data):
        response_line = data.split("\r\n\r\n")[0]
        code = int(response_line.split(" ")[1]) # gets 200 or 404 from middle
        return code

    def get_headers(self,data):
        headers_arr = []
        splitted_arr = data.split("\r\n")
        #https://stackoverflow.com/questions/627435/how-to-remove-an-element-from-a-list-by-index HOW to remove by index
        splitted_arr.pop(0)
        end = splitted_arr.index('')
        splitted_arr = splitted_arr[:end]
        for header_line in splitted_arr:
            header_info_content = header_line.split(': ', 1) # Only split first occurance in case of colons inside header values like expiry tokens etc
            headers_arr.append(header_info_content)

        return headers_arr

    def get_body(self, data):
        body= data.split("\r\n\r\n")[1]
        return body

        return None
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            print(sock)
            part = sock.recv(1024)
            # print("Part ", part)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        decoded = buffer.decode('utf-8')
        # print("\n\n\n\nBUFFER__DECODED!!!\n\n\r\n\r", decoded)
        # print(decoded[9:12])
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
       # print("URL: ", url)
        # temp_host = urllib.parse.urlparse(url)
        # host = '{uri.scheme}://{uri.netloc}/'.format(uri=temp_host)
        host = urllib.parse.urlparse(url).hostname
        #print(host)
        port = urllib.parse.urlparse(url).port
        if port is None:
            port = 80
        path = urllib.parse.urlparse(url).path
        if path == "":
            path = "/"
        request = "GET %s HTTP/1.1\r\nHost: %s\r\nConnection: close\r\n\r\n" % (path, host)
        #@print(request)
        self.connect(host, port)
        self.sendall(request)
        # print("SOCKET:   ",self.socket, "\n\n")
        response = self.recvall(self.socket)
        self.close()

        code = self.get_code(response)
        body = self.get_body(response)
        # print(response)
        #exit()
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        host = urllib.parse.urlparse(url).hostname
        port = urllib.parse.urlparse(url).port
        if port is None:
            port = 80
        path = urllib.parse.urlparse(url).path
        if path == "":
            path = "/"

        content = ''
        # args contains postable content
        if args is not None:
            for key in args:
                content += str(key) + "=" + str(args[key]) + "&"
            content = content[:-1]
            #print(content)
        content_len = str(len(content))
        request = "POST %s HTTP/1.1\r\nHost: %s\r\nContent-Type: application/x-www-form-urlencoded\r\nContent-Length: %s\r\nConnection: close\r\n\r\n%s" % (path, host, content_len, content)
        self.connect(host, port)
        self.sendall(request)
        response = self.recvall(self.socket)
        self.close()

        body = self.get_body(response)
        code = self.get_code(response)

        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        #print("3\n")
        (client.command( sys.argv[2], sys.argv[1] ))
    else:
        #print("other\n")
        (client.command( sys.argv[1] ))
