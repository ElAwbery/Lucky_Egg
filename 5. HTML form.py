#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 17:38:44 2018
@author: ElAwbery
"""
'''
write the html form and test that it works by adding it to the html body in a dictinary entry
'''

import http.server
import socketserver

PORT = 80

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
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

    html_form = '''
<form>
<p><label> You have </label><input type="number" style="width: 50px"> Squirtles </label></p>
<p><label> You have </label><input type="number" style="width: 50px"> Squirtle candy </label></p>
<p><button>Update</button></p>
</form>
'''

    def do_GET(self):
        """
        Creates a page from html boilerplate plus page-specific html. 
        If url not found, returns 404 error message. 
        """
        path = self.path
        
        # dictionary maps paths to body html
        pokemon = {'/squirtle': """Squirtle<br> Squirtle evolves into a<a href ="wartortle">Wartortle</a><br> Its third evolution is a <a href ="blastoise">Blastoise.</a>""" + self.html_form,
                   '/wartortle': """Wartortle<br> Wartortle is the second evolution of the <a href ="squirtle">Squirtle</a><br> Wartortle evolves into a <a href ="blastoise">Blastoise.</a>""",
                   '/blastoise': """Blastoise<br> Blastoise is the third evolution of the <a href ="squirtle">Squirtle.</a><br> It evolves from a <a href ="wartortle">Wartortle.</a>""",}
        
        # if the url is known, find the html string and write the file:
        if path in pokemon:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            html = self.boilerplate_prefix + pokemon[path] + self.boilerplate_suffix
            self.wfile.write(html.encode('utf-8')) 
            
        else:
            self.send_error(http.HTTPStatus.NOT_FOUND, "Pokemon Not Found".format(self.path))
       
        
# set up an socket server at PORT 80, specify the handler for the port, wait for a url request 

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
   print("serving at port", PORT)
   # an infinite loop of waiting for a request
   httpd.serve_forever()
   
