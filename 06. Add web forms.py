#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 15:51:01 2018
@author: ElAwbery
"""

import http.server
import socketserver

PORT = 80

# Page classes standardize different page formulas. 

class pokemon(object):
    """
    A Pokemon object is used to construct the body of a web page representing
    that species
    """
    def __init__(self, name, first_stage = None, second_stage = None, third_stage = None):
        self.name = name
        self.first_stage = first_stage
        self.second_stage = second_stage
        self.third_stage = third_stage
        
    def name_to_object(self, name):
        """Retrieves stored Pokemon instance from string name"""
        return PokemonHandler.pokemon_dictionary[name]
    
    def __str__(self):
        return self.name + " is a Pokemon"

class first_stage(pokemon):
    
    # All the pokemon in an evolutionary sequence share the same candy type,
    # so only the first stage keeps track of the candy count. So only the
    # first stage class should initialize that.
    def __init__(self, name, first_stage = None, second_stage = None, third_stage = None):
        pokemon.__init__(self, name, first_stage, second_stage, third_stage)
        self.candies = 0
        
    def update_candy_count(self, candies):
        """
        candies, a positive or negative integer
        """
        self.candies = candies
        return self.candies    
        
    def html_body(self):
        return self.name +'<br>' + self.name + " is a first stage Pokemon." \
    + '<br>' + self.name + " evolves into a <a href =" + self.second_stage \
    + ">" + self.second_stage + " </a><br>" + "Its third stage is a <a href ="\
    + self.third_stage + ">" + self.third_stage + " </a><br>" + '''
<form>
<p><label> You have </label><input type="number" style="width: 50px"> '''\
 + self.name +'s' + '''</label></p>
<p><button>Update</button></p>
<p><label> You have </label><input type="number" style="width: 50px"> '''\
 + self.name + ' candies' '''</label></p>
<p><button>Update</button></p>
</form>
'''
        
class second_stage(pokemon):
    
    def html_body(self):
        return self.name +'<br>' + self.name + " is a second stage Pokemon."\
    + '<br>' + self.name + " evolves from a <a href =" + self.first_stage \
    + ">" + self.first_stage + " </a><br>" + "Its third stage is a <a href ="\
    + self.third_stage + ">" + self.third_stage + " </a><br>" + '''
<form>
<p><label> You have </label><input type="number" style="width: 50px"> '''\
 + self.name +'s' + '''</label></p>
<p><button>Update</button></p>
<p><label>''' + self.name + ''' uses ''' + self.first_stage + \
''' candy. You have ''' + str(self.name_to_object(self.first_stage).candies) +\
''' of them.</label></p>
</form>
'''
  
class third_stage(pokemon):
    
    def html_body(self):
        return self.name +'<br>' + self.name + " is a third stage Pokemon"\
    + '<br>' + self.name + " evolves from a <a href =" + self.second_stage\
    + ">" + self.second_stage + " </a><br>" + "Its first stage is a <a href ="\
    + self.first_stage + ">" + self.first_stage + " </a><br>" + '''
<form>
<p><label> You have </label><input type="number" style="width: 50px"> '''\
 + self.name +'s' + '''</label></p>
<p><button>Update</button></p>
<p><label>''' + self.name + ''' uses ''' + self.first_stage\
 + ''' candy. You have </label><input type="number" style="width: 50px"> '''\
 +  str(self.name_to_object(self.first_stage).candies) + ' of them.' '''</label></p>
</form>
'''


class PokemonHandler(http.server.SimpleHTTPRequestHandler):
    
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
    
    pokemon_dictionary = {'Squirtle': first_stage('Squirtle', 'Squirtle', 'Wartortle', 'Blastoise'), 
                          'Wartortle': second_stage('Wartortle', 'Squirtle', 'Wartortle', 'Blastoise'),
                          'Blastoise': third_stage('Blastoise', 'Squirtle', 'Wartortle', 'Blastoise'),
                          'Pichu': first_stage('Pichu', 'Pichu', 'Pikachu', 'Raichu'),
                          'Pikachu': second_stage('Pikachu', 'Pichu', 'Pikachu', 'Raichu'),
                          'Raichu': third_stage('Raichu', 'Pichu', 'Pikachu', 'Raichu')}
    
    def do_GET(self):
        """
        Creates a page from html boilerplate plus page-specific html. 
        If url not found, returns 404 error message. 
        """
        path = self.path
        name = path[1:]
        
        # if the url is known, find the html string and write the file:
        if name in self.pokemon_dictionary:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            html = self.boilerplate_prefix + self.pokemon_dictionary[name].html_body() + self.boilerplate_suffix
            self.wfile.write(html.encode('utf-8')) 
            
        else:
            self.send_error(http.HTTPStatus.NOT_FOUND, "Pokemon Not Found".format(self.path))
       
        
# set up an OS connection at PORT 80, specify the handler for the port, wait for a url request 

with socketserver.TCPServer(("", PORT), PokemonHandler) as httpd:
   print("serving at port", PORT)
   # an infinite loop of waiting for a request
   httpd.serve_forever()
   
