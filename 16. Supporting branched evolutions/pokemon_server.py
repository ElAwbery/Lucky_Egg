#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 15:17:03 2019

@author: ElAwbery
"""
import http.server
import socketserver

"""
Server code has been separated from the application code: in previous versions
they were entangled and the do_GET and do_POST handlers were pokemon-specific.
In principle this version can process any browser request and call the  
application's router methods.
The web server connection is wrapped in a web_server function called by 
the application code, and no longer runs on loading. 
"""

PORT = 80

    
# Source code for the HTTPRequestHandler class: 
# https://github.com/python/cpython/blob/2.7/Lib/ƒHTTPServer.py
# "  - rfile is a file object open for reading positioned at the start of 
# the optional input data part "
               
# Python documentation for working with streams: 
# https://docs.python.org/3/library/io.html

"""
The applicationHandler class is a generic interface between the browser and 
our application code. 
"""

class applicationHandler(http.server.SimpleHTTPRequestHandler):
    """
    Sends get and post requests to application code.
    Sends pages to the web browser.
    """
    
    def parse_http_arguments(self, string):
        """
        Takes a single string of user input from an HTML form.
        The string is keyword=value pairs separated by &s.
        Returns a dictionary of the keyword/value pairs.
        """
        
        new_data = {}
        # create a list with two elements
        key_value_pairs = string.split('&')
        
        for pair in key_value_pairs:
            key_value = pair.split('=')
            key = key_value[0]
            value = key_value[1]
            if value == '':
                value = 0
            new_data[key] = value
        
        return(new_data)
        
    
    def do_GET(self):
        """
        Called by the server when the browser sends a GET request.
        Gets content_type (which goes in the header: html, css or error message) 
        and response contents from the application's router.
        Sends that to browser.
        """
        (content_type, page) = self.get_router()
        
        assert type(content_type) == str and type(page) == str
        
        if content_type == 'error':
            self.send_error(http.HTTPStatus.NOT_FOUND, page.format(self.path))

        else:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(page.encode('utf-8')) 
        
    def do_POST(self):
        """
        Called by the server when the browser sends a POST request.
        Cleans up request and sends its contents to the application's router.
        Sends application's response to the browser.
        """
        
        # self.rfile is the data string. It's an io.BufferedReader object 
        # (a binary object).
        # io.BufferedReader has a read method that requires a length argument.
        # self.headers gets the http headers as a dict. Content-Length is one 
        # of the headers, a dict key, the length of the data string. 
        # All header values are strings, so we coerce it to an int.
        # The read method returns a python bytes object, not a python string, 
        # so we have to convert it using the decode method.
        
        user_update = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        
        self.arguments = self.parse_http_arguments(user_update)
        
        (content_type, page) = self.post_router()
        
        if content_type == 'error':
            self.send_error(http.HTTPStatus.NOT_FOUND, page.format(self.path))
        
        else: 
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", content_type)
            self.end_headers()
            self.wfile.write(page.encode('utf-8'))
            
# The default TCPServer catches errors, which is sensible on a server but makes
# debugging difficult. This subclass overrides the method that includes the
# error handler.
class TCPServer_no_error_handling(socketserver.TCPServer):
   def _handle_request_noblock(self):
       """
       Version of _handle_request_noblock() that does not catch errors.
       """
       try:
           request, client_address = self.get_request()
       except OSError:
           return
       if self.verify_request(request, client_address):
           self.process_request(request, client_address)
       else:
           self.shutdown_request(request)
            
# set up an OS connection at PORT 80, specify the handler for the port, wait for a url request 
def web_server(handler):
    with TCPServer_no_error_handling(("", PORT), handler) as httpd:
        print("serving at port", PORT)
        # an infinite loop of waiting for a request
        httpd.serve_forever()

        
