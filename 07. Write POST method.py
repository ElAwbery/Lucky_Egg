#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 13:44:26 2018
@author: ElAwbery
""" 

""" 
Extending the previous work:
Implements the post method of the request handler class. 
Your page class will have data attributes that can be modified by the client. 
The data from the client will be stored as local state within the page class.
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
        self.count = 0
        
    def name_to_object(self, name):
        """
        Retrieves stored Pokemon instance from string name
        """
        return PokemonHandler.pokemon_dictionary[name][0]
    
    def set_pokemon_count(self, new_count):
        """
        new_count is an int, passed by PokemonHandler.do_POST
        updates and returns Pokemon count
        """
        self.count = new_count
        return self.count
    
    def __str__(self):
        return self.name + " is a Pokemon"
    
class first_stage(pokemon):
    
    # All the pokemon in an evolutionary sequence share the same candy type,
    # so only the first stage keeps track of the candy count. So only the
    # first stage class should initialize the candy count.
    def __init__(self, name, first_stage = None, second_stage = None, third_stage = None):
        pokemon.__init__(self, name, first_stage, second_stage, third_stage)
        self.candies = 0
        
    def set_candy_count(self, candies):
        """
        candies, a positive or negative integer
        """
        self.candies = candies
        return self.candies    
        
    def html_body(self):
        return self.name + ":" + '<br><br>' + self.name + " is a first stage Pokemon." \
    + '<br>' + self.name + " evolves into a <a href =" + self.second_stage \
    + ">" + self.second_stage + " </a><br>" + "Its third stage is a <a href ="\
    + self.third_stage + ">" + self.third_stage + " </a><br><br>"\
+ '''
<form action="/''' + self.name +'"' + '''method="post" + >
<div>
You have 
<label for="new_count">
<input type="number" name="new_count" value = "'''+ str(self.count)\
+ '''" min="0" style="width: 50px"> ''' + " " + self.name + "s"\
+ '''</label>
and''' + " " + '''
<label for="new_candies">
<input type="number" name="new_candies" value = "'''+ str(self.candies)\
+ '''"min="0" style="width: 50px">''' + " " + self.name + ''' candies.
</label>
</div>
<br>
<div class="button">
<button type="submit">Update</button>
</div>
</form>
'''    

class second_stage(pokemon):
    
    def html_body(self):
        return self.name + ":" + '<br><br>' + self.name + " is a second stage Pokemon."\
    + '<br>' + self.name + " evolves from a <a href =" + self.first_stage \
    + ">" + self.first_stage + " </a><br>" + "Its third stage is a <a href ="\
    + self.third_stage + ">" + self.third_stage + " </a><br><br>"\
    + self.name + ' uses ' + self.first_stage + " candies. You have "\
    + str(self.name_to_object(self.first_stage).candies) + " of them."\
    + '<br><br>' + '''
    
<form action="/''' + self.name +'"' + '''method="post" + >
<div>
You have 
<label for="new_count">
<input type="number" name="new_count" value = "'''+ str(self.count)\
+ '''" min="0" style="width: 50px"> ''' + " " + self.name + "s"\
+ '''</label>
</div>
<br>
<div class="button">
<button type="submit">Update</button>
</div>
</form>
'''   
    
class third_stage(pokemon):
    
    def html_body(self):
        return self.name + ":" + '<br><br>' + self.name + " is a third stage Pokemon"\
    + '<br>' + self.name + " evolves from a <a href =" + self.second_stage\
    + ">" + self.second_stage + " </a><br>" + "Its first stage is a <a href ="\
    + self.first_stage + ">" + self.first_stage + " </a><br><br>"\
    + self.name + ' uses ' + self.first_stage + " candies. You have "\
    + str(self.name_to_object(self.first_stage).candies) + " of them."\
    + '<br><br>' + '''
    
<form action="/''' + self.name +'"' + '''method="post" + >
<div>
You have 
<label for="new_count">
<input type="number" name="new_count" value = "'''+ str(self.count)\
+ '''" min="0" style="width: 50px"> ''' + " " + self.name + "s"\
+ '''</label>
</div>
<br>
<div class="button">
<button type="submit">Update</button>
</div>
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

    pokemon_dictionary = {'Squirtle': [first_stage('Squirtle', 'Squirtle', 'Wartortle', 'Blastoise')], 
                          'Wartortle': [second_stage('Wartortle', 'Squirtle', 'Wartortle', 'Blastoise')],
                          'Blastoise': [third_stage('Blastoise', 'Squirtle', 'Wartortle', 'Blastoise')],
                          'Pichu': [first_stage('Pichu', 'Pichu', 'Pikachu', 'Raichu')],
                          'Pikachu': [second_stage('Pikachu', 'Pichu', 'Pikachu', 'Raichu')],
                          'Raichu': [third_stage('Raichu', 'Pichu', 'Pikachu', 'Raichu')]}
    
    def name_to_object(self, name):
        """Retrieves stored Pokemon instance from string name"""
        return self.pokemon_dictionary[name][0]  
    
    def parse_http_arguments(self, string):
        """Takes a single string of user input from an HTML form
        The string is keyword=value pairs separated by &s
        Returns a dictionary of the keyword/value pairs
        """
        # create a list with two elements
        new_data = {}
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
        Generates a pokemon page from html boilerplate plus page-specific html. 
        If url not found, returns 404 error message. 
        """
        path = self.path
        name = path[1:]         # strip the leading slash
        
        # if the path is the name of a known pokemon, get its html string and construct the response:
        if name in self.pokemon_dictionary:
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            html = self.boilerplate_prefix + self.pokemon_dictionary[name][0].html_body() + self.boilerplate_suffix
            self.wfile.write(html.encode('utf-8')) 
            
        else:
            self.send_error(http.HTTPStatus.NOT_FOUND, "Pokemon Not Found".format(self.path))

    # Source code for the HTTPRequestHandler class: 
    # https://github.com/python/cpython/blob/2.7/Lib/BaseHTTPServer.py
    # "  - rfile is a file object open for reading positioned at the start of the optional input data part "
                
    # Python documentation for working with streams: https://docs.python.org/3/library/io.html
         
    def do_POST(self):
        
        '''
        Processes a POST request to update the count of pokemons and/or candies of a species
        '''
        path = self.path
        name = path[1:]    # strip leading slash
        
        # self.rfile is the data string. It's an io.BufferedReader object (a binary object).
        # io.BufferedReader has a read method that requires a length argument.
        # self.headers gets the http headers as a dict. Content-Length is one of the headers, a dict key, 
        # the length of the data string. All header values are strings, so we coerce it to an int.
        # the read method returns a python bytes object, not a python string, 
        # so we have to convert it using the decode method.
        
        if name in self.pokemon_dictionary:
        
            user_update = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
            
            parsed = self.parse_http_arguments(user_update)
            
            # Update data in the pokemon class
            if 'new_candies' in parsed:
                self.name_to_object(name).set_candy_count(int(parsed['new_candies']))
            
            self.name_to_object(name).set_pokemon_count(int(parsed['new_count']))
        
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            html = (self.boilerplate_prefix + "Updated:<br><br>"
                    + self.pokemon_dictionary[name][0].html_body() + self.boilerplate_suffix)
            self.wfile.write(html.encode('utf-8')) 
            
        else:
            self.send_error(http.HTTPStatus.NOT_FOUND, "Sorry, something went wrong.".format(self.path))
       
# set up an OS connection at PORT 80, specify the handler for the port, wait for a url request 

with socketserver.TCPServer(("", PORT), PokemonHandler) as httpd:
   print("serving at port", PORT)
   # an infinite loop of waiting for a request
   httpd.serve_forever()
