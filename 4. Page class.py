#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 15:51:01 2018
@author: ElAwbery
"""

import http.server
import socketserver

PORT = 80

# Define the page class. Page classes standardize different page formulas. 

class pokemon(object):
    """Charlie
    A Pokemon object is used to construct the body of a web page representing
    that species
    """
    def __init__(self, name, first_stage = None, second_stage = None, third_stage = None):
        self.name = name
        self.first_stage = first_stage
        self.second_stage = second_stage
        self.third_stage = third_stage
    
    def update_candy_count(self, candies):
        """
        candies, a positive or negative integer
        """
        self.candies = candies
        return candies
               
    def __str__(self):
        return self.name + " is a Pokemon"

class first_stage(pokemon):
    
    # All the pokemon in an evolutionary sequence share the same candy type,
    # so only the first stage keeps track of the candy count. So only the
    # first stage class should initialize that.
    def __init__(self, name, first_stage = None, second_stage = None, third_stage = None):
        pokemon.__init__(self, name, first_stage, second_stage, third_stage)
        self.candies = 0
    
    def html_body(self):
        return self.name +'<br>' + self.name + " is a first stage Pokemon." \
    + '<br>' + self.name + " evolves into a <a href =" + self.second_stage \
    + ">" + self.second_stage + " </a><br>" + "Its third stage is a <a href ="\
    + self.third_stage + ">" + self.third_stage + " </a><br>"
        
class second_stage(pokemon):
    
    def html_body(self):
        return self.name +'<br>' + self.name + " is a second stage Pokemon."\
    + '<br>' + self.name + " evolves from a <a href =" + self.first_stage \
    + ">" + self.first_stage + " </a><br>" + "Its third stage is a <a href ="\
    + self.third_stage + ">" + self.third_stage + " </a><br>"
  
class third_stage(pokemon):
    
    def html_body(self):
        return self.name +'<br>' + self.name + " is a third stage Pokemon"\
    + '<br>' + self.name + " evolves from a <a href =" + self.second_stage\
    + ">" + self.second_stage + " </a><br>" + "Its first stage is a <a href ="\
    + self.first_stage + ">" + self.first_stage + " </a><br>"


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
    
    def do_GET(self):
        """
        Creates a page from html boilerplate plus page-specific html. 
        If url not found, returns 404 error message. 
        """
        path = self.path
        name = path[1:]
        
        # Dictionary maps paths to body html
        # In this implementation, for simplicity we construct all the web pages
        # on every GET request and select one. Not feasible, for performance
        # reasons, on a large web site; soon we'll change this.
        pokemon = {'Squirtle': first_stage('Squirtle', 'Squirtle', 'Wartortle', 'Blastoise').html_body(),
                   'Wartortle': second_stage('Wartortle', 'Squirtle', 'Wartortle', 'Blastoise').html_body(),
                   'Blastoise': third_stage('Blastoise', 'Squirtle', 'Wartortle', 'Blastoise').html_body(),
                   'Pichu': first_stage('Pichu', 'Pichu', 'Pikachu', 'Raichu').html_body(),
                   'Pikachu': second_stage('Pikachu', 'Pichu', 'Pikachu', 'Raichu').html_body(),
                   'Raichu': third_stage('Raichu', 'Pichu', 'Pikachu', 'Raichu').html_body(),}
        
        # if the url is known, find the html string and write the file:
        if name in pokemon:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            
            html = self.boilerplate_prefix + pokemon[name] + self.boilerplate_suffix
            self.wfile.write(html.encode('utf-8')) 
            
        else:
            self.send_error(http.HTTPStatus.NOT_FOUND, "Pokemon Not Found".format(self.path))
       
        
# set up an OS connection at PORT 80, specify the handler for the port, wait for a url request 

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
   print("serving at port", PORT)
   # an infinite loop of waiting for a request
   httpd.serve_forever()
   
