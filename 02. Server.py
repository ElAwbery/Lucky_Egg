#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 12:20:16 2018
@author: ElAwbery
"""

# This code bypasses commercial web servers and creates a server on my computer
# It's the minimal code required to invoke the http server side library

# Python documentation for the http.server: https://docs.python.org/3/library/http.server.html

import http.server
import socketserver

PORT = 80

# Boilerplate variables for an html page

boilerplate_prefix = '''<!DOCTYPE html>
<html lang="en">
 <head>
   <meta charset="utf-8">
 </head>
 <body>
'''
boilerplate_suffix = '''
 </body>
</html>'''

# The server in its simplest form, a request handler
# receives a url from the socket handler and sends back a response with the html 

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
   def do_GET(self):
       """Serve a GET request."""
       self.send_response(http.HTTPStatus.OK)
       self.send_header("Content-type", 'text/html')
       self.end_headers()
       # create the html string:
       html = boilerplate_prefix + "The URL requested was: " + self.path + boilerplate_suffix 
       # convert the html string to a bytes object and send it to the socket:
       self.wfile.write(html.encode('utf-8')) 
       
       
# set up a socket server at PORT 80, specify the handler for the port, wait for a url request 

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
   print("serving at port", PORT)
   # an infinite loop of waiting for a request
   httpd.serve_forever()
