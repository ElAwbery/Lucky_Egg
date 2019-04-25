#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 15:53:24 2019

@author: ElAwbery
"""

""" 
Extending the previous work:
Write database load and save methods
"""

# Importlib needed in order to import mysql.connector
# Spyder gives a 'not used' alarm because it doesn't know it's being used 
# behind the scenes

import http.server
import socketserver
import importlib
import mysql.connector


PORT = 80

# Page classes standardize different page formulas. 

class pokemon(object):
    """
    A Pokemon object is used to construct the body of a web page representing
    that species
    """
    def __init__(self, name, count, candies, first_stage = None, second_stage = None, 
                 third_stage = None):
        self.name = name
        self.first_stage = first_stage
        self.second_stage = second_stage
        self.third_stage = third_stage
        self.count = count
        self.candies = candies
        self.status_line = ""
        
    # Removed name_to_object method, replaced by global save
        
    def set_pokemon_count(self, new_count):
        """
        new_count is an int
        updates Pokemon count and saves to database
        """
        self.count = new_count
        save_to_database(self)
    
    def set_candies(self, candies):
        """
        candies, a positive integer
        """
        self.candies = candies
        save_to_database(self)
        
        # The second and third stages share candies with the first, so we
        # update those together here 
        # Save candy count of the first stage object to second and third stage
        # rows in database
        
        second = load(self.second_stage)
        second.candies = candies
        save_to_database(second)
        
        third = load(self.third_stage)
        third.candies = candies
        save_to_database(third)
        
        # Candy count return not needed now. All data accessed via load method.
    
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
    
    
class first_stage(pokemon):
       
    def html_body(self):
        return self.template_substitute('''
<h1>$name$</h1>
$status_line$
<p>$name$ is a first stage Pokemon.</p>
<p>$name$ evolves into a <a href = $second_stage$>$second_stage$</a></p>
<p>Its third stage is a <a href = $third_stage$>$third_stage$</a></p>

<form action="$name$" method="post">
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0"> $name$s
    and
    <input type="number" name="new_candies" value = "$candies$" min="0"> $name$ candies.
  </p>
  <button type="submit">Update</button>
</form>
''')
        
class second_stage(pokemon):
    
    def html_body(self):
        return self.template_substitute('''
<h1>$name$</h1>
$status_line$
<p>$name$ is a second stage Pokemon.</p> 
<p>$name$ evolves from a <a href = $first_stage$>$first_stage$</a></p> 
<p>Its third stage is a <a href = $third_stage$>$third_stage$</a><br></p> 
<p>$name$ uses <a href = $first_stage$>$first_stage$</a> candies. You have $candies$ of them.<br></p> 

<form action="$name$" method="post">                     
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0"> $name$s
  </p>
  <button type="submit">Update</button>
</form>
''')   
       
class third_stage(pokemon):
    
    def html_body(self):
        return self.template_substitute('''
<h1>$name$</h1>
$status_line$
<p>$name$ is a third stage Pokemon.</p>
<p>$name$ evolves from a <a href = $second_stage$>$second_stage$</a></p>
<p>Its first stage is a <a href = $first_stage$>$first_stage$</a></p>
<p>$name$ uses <a href = $first_stage$>$first_stage$</a> candies. You have $candies$ of them.</p>

<form action="$name$" method="post">                     
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0"> $name$s
  </p>
  <button type="submit">Update</button>
</form>
''')   


def load(name):
    """
    Name is name of a pokemon species
    Retrieves the corresponding row of pokemon attributes from the database
    Constructs the pokemon object from the data
    """
    assert type(name) == str
    
    # Create a connection to the mysql server
    # These are the default login details
    # Port 8889 is the port MAMP uses to connect to MySQL
    # This recreates the connection on every load, which is inefficient but OK for now
    cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1', port="8889",
                              database='Pokemon')
    
    # Tell the cnx connection to create a cursor object
    # All database action is later assigned to the cursor
    cursor = cnx.cursor()
    cursor.execute("SELECT * from Pokemon WHERE name = '" + name + "';")
    row = cursor.fetchone()
    name = row[0]
    first = row[1]
    second = row[2]
    third = row[3]
    count = row[4]
    candies = row[5]
    
    # This is clunky, it will be cleaner after refactoring classes
    if name == first:
        pokemon_object = first_stage(name, count, candies, first, second, third)
        
    elif name == second:
        pokemon_object = second_stage(name, count, candies, first, second, third)
        
    elif name == third:
        pokemon_object = third_stage(name, count, candies, first, second, third)
        
    else:
        pokemon_object = pokemon(name, count, candies, first, second, third)
        
    # Close the cursor and connection to tidy up
    cursor.close()
    cnx.close()
    
    return pokemon_object

    
def save_to_database(pokemon_object):
    """
    Opens the database
    Creates a cursor
    Takes pokemon object as argument, and stores its attributes to database row
    """
    assert isinstance (pokemon_object, pokemon)
        
    # Create a connection to the mysql server
    cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1', port="8889",
                              database='Pokemon')
    
    cursor = cnx.cursor()
    
    name = pokemon_object.name
    first = pokemon_object.first_stage
    second = pokemon_object.second_stage
    third = pokemon_object.third_stage
    count = pokemon_object.count
    candies = pokemon_object.candies

    cursor.execute("UPDATE Pokemon SET `Name` =  '" + name + "', `First stage`\
                   =  '" + first + "', `Second stage` =  '" + second + "',\
                   `Third stage` =  '" + third + "',\
                   `Count` =  '" + str(count) + "',\
                   `Candies` =  '" + str(candies) + "' WHERE `Name` =  '" + name + "';") 
           
    # Alternatively could set connection to autocommit; we don't need multi-statement transactions here        
    cnx.commit()
    # Close the cursor and database to tidy up
    cursor.close()
    cnx.close()


class PokemonHandler(http.server.SimpleHTTPRequestHandler):
    
    # Boilerplate prefix and suffix for an html page
    boilerplate_prefix = '''<!DOCTYPE html>
<html lang="en">
 <head>
   <meta charset="utf-8">
   <link href="pokemon_page.css" rel="stylesheet" type="text/css"/>
 </head>
 <body>
'''
    boilerplate_suffix = '''
 </body>
</html>'''

    # Pokemon_dictionary, in previous version, is now replaced by database
    # Handler name_to_object method replaced by global load function

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
        
        # send css
        if name == "pokemon_page.css":
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/css')
            self.end_headers()
            html = '''.status_line {
              margin:30px;
              border:2px solid #006600;
              padding:10px;
              font-family:Constantia,Georgia,"Times New Roman","Times Roman",Times,TimesNR,serif;
              font-size:25px;
              color:#006600; 
              text-align:center; 
              background-color:#dbffb6; 
              width:450px;
             }
            h1 {
              font-family:Constantia,Georgia,"Times New Roman","Times Roman",Times,TimesNR,serif;
              font-size:40px; font-style:italic;
            }
            input {
              width:50px;
            }'''
            self.wfile.write(html.encode('utf-8')) 
        
        # if the path is the name of a known pokemon, get its html string and construct the response:
        else:
            try:
                self.send_response(http.HTTPStatus.OK)
                self.send_header("Content-type", 'text/html')
                self.end_headers()
                html = self.boilerplate_prefix + load(name).html_body() + self.boilerplate_suffix
                self.wfile.write(html.encode('utf-8')) 
            except:
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
        
        user_update = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        
        parsed = self.parse_http_arguments(user_update)
        
        # Update data in the pokemon class
        try:
            loaded = load(name)
            
            if 'new_candies' in parsed:
                loaded.set_candies(int(parsed['new_candies']))
            
            # Every update sets the count, whereas only first-stage updates set candies
            loaded.set_pokemon_count(int(parsed['new_count']))
            loaded.status_line = '''<p class="status_line">Updated</p>'''
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            html = (self.boilerplate_prefix + loaded.html_body() + self.boilerplate_suffix)
            self.wfile.write(html.encode('utf-8')) 
            
            # Clear the status line so that it does not show as
            # updated in subsequent GET requests
            load(name).status_line = ""
                
        # 404 error: load method failed
        except:
            self.send_error(http.HTTPStatus.NOT_FOUND, \
                            "Could not set candies for this Pokemon family.".format(self.path))
                
# set up an OS connection at PORT 80, specify the handler for the port, wait for a url request 

with socketserver.TCPServer(("", PORT), PokemonHandler) as httpd:
   print("serving at port", PORT)
   # an infinite loop of waiting for a request
   httpd.serve_forever()
   


