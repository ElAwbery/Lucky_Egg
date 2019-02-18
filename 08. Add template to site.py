#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 16 13:44:26 2018
@author: ElAwbery
""" 

""" 
Extending the previous work:
Adds templates to the html constructor in each stage class.
Defines a template substitution method for the pokemon parent class. 
Cleans up the html. 
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
    def __init__(self, name, first_stage = None, second_stage = None, 
                 third_stage = None):
        self.name = name
        self.first_stage = first_stage
        self.second_stage = second_stage
        self.third_stage = third_stage
        self.count = 0
        self.candies = 0
        
    def name_to_object(self, name):
        """
        Retrieves stored Pokemon instance from string name
        """
        return PokemonHandler.pokemon_dictionary[name]
    
    def set_pokemon_count(self, new_count):
        """
        new_count is an int, passed by PokemonHandler.do_POST
        updates and returns Pokemon count
        """
        self.count = new_count
        return self.count
    
    def template_substitute(self, template):
        """
        Takes an html string template and substitutes values for variables.
        Returns html string
        """
        # If the number of $ is not even, raise an error; template format wrong. 
        assert template.count('$')%2 == 0 
            
        # List of strings; every second string represents a variable requiring value substitution 
        template_segments = template.split('$')
        
        # If the template starts with a variable, add a dummy to the beginning of 
        # the list to ensure the invariant that odd numbered entries are literals
        if template[0] == '$':
            template_segments = [''] + template_segments
        
        html = ''
        
        # Construct an html string with substituted variable values 
        index = 0
        while index < len(template_segments):
            # Keep literal parts of the template 
            if index%2 == 0:
                html += template_segments[index]
                
            # Substitute the variable value, ensuring it is a string
            else:
                new_value = getattr(self, template_segments[index])
                
                if isinstance(new_value, int):
                    new_value = str(new_value)
                    
                if not isinstance(new_value, str):
                    raise TypeError
    
                html += new_value
                    
            index += 1
    
        return html
        
    def __str__(self):
        return self.name + " is a Pokemon"


class first_stage(pokemon):
    
    # All the pokemon in an evolutionary sequence share the same candy type,
    # so only the first stage keeps track of the candy count. So only the
    # first stage class should initialize the candy count.
    
    def __init__(self, name, first_stage = None, second_stage = None, third_stage = None):
        pokemon.__init__(self, name, first_stage, second_stage, third_stage)
        self.candies = 0
        
    def set_candies(self, candies):
        """
        candies, a positive or negative integer
        """
        self.candies = candies
        # The second and third stages share candies with the first, so we
        # update those here. 
        self.name_to_object(self.second_stage).candies = candies
        self.name_to_object(self.third_stage).candies = candies

        return self.candies
        
    def html_body(self):
        return self.template_substitute('''
<h1>$name$</h1>
<p>$name$ is a first stage Pokemon.</p>
<p>$name$ evolves into a <a href = $second_stage$>$second_stage$</a></p>
<p>Its third stage is a <a href = $third_stage$>$third_stage$</a></p>
<form action="$name$" method="post">
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0" style="width: 50px"> $name$s
    and
    <input type="number" name="new_candies" value = "$candies$" min="0" style="width: 50px"> $name$ candies.
  </p>
  <button type="submit">Update</button>
</form>
''')


class second_stage(pokemon):
    
    def html_body(self):
        return self.template_substitute('''
<h1>$name$</h1>
 
<p>$name$ is a second stage Pokemon.</p> 
<p>$name$ evolves from a <a href = $first_stage$>$first_stage$</a></p> 
<p>Its third stage is a <a href = $third_stage$>$third_stage$</a><br></p> 
<p>$name$ uses <a href = $first_stage$>$first_stage$</a> candies. You have $candies$ of them.<br></p> 
<form action="$name$" method="post">                     
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0" style="width: 50px"> $name$s
  </p>
  <button type="submit">Update</button>
</form>
''')   
    
  
class third_stage(pokemon):
    
    def html_body(self):
        return self.template_substitute('''
<h1>$name$</h1>
<p>$name$ is a third stage Pokemon.</p>
<p>$name$ evolves from a <a href = $second_stage$>$second_stage$</a></p>
<p>Its first stage is a <a href = $first_stage$>$first_stage$</a></p>
<p>$name$ uses <a href = $first_stage$>$first_stage$</a> candies. You have $candies$ of them.</p>
<form action="$name$" method="post">                     
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0" style="width: 50px"> $name$s
  </p>
  <button type="submit">Update</button>
</form>
''')   


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
    
    def name_to_object(self, name):
        """Retrieves stored Pokemon instance from string name"""
        return self.pokemon_dictionary[name]  
    
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
            html = self.boilerplate_prefix + self.pokemon_dictionary[name].html_body() + self.boilerplate_suffix
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
                self.name_to_object(name).set_candies(int(parsed['new_candies']))
            
            self.name_to_object(name).set_pokemon_count(int(parsed['new_count']))
        
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            html = (self.boilerplate_prefix + "Updated:<br><br>"
                    + self.pokemon_dictionary[name].html_body() + self.boilerplate_suffix)
            self.wfile.write(html.encode('utf-8')) 
            
        else:
            self.send_error(http.HTTPStatus.NOT_FOUND, "Sorry, something went wrong.".format(self.path))
        
# set up an OS connection at PORT 80, specify the handler for the port, wait for a url request 

with socketserver.TCPServer(("", PORT), PokemonHandler) as httpd:
   print("serving at port", PORT)
   # an infinite loop of waiting for a request
   httpd.serve_forever()
