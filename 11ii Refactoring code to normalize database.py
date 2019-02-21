#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 14:59:45 2019

@author: ELAwbery
"""

"""
An exercise in refactoring:
The database is inefficient because it stores the same data multiple times.
We want each class with unique data attributes to have its own
table in the database.

1. Write an ORM_object class to interface with the database. 
It will include load and store methods for our classes. 

In principle we want to keep our application code separate from our database 
operations. So the ORM_object class will have no code specific to an application 
object type and our application code will not know any information specific 
to the database.  

2. Refactor the class structure to two subclasses of the ORM_object class, 
pokemon_family and pokemon_species.

The pokemon_family class will keep track of candy counts and family members 
which are pokemon_species objects. 

The pokemon_species class will keep track of individual pokemon counts. Because 
the family class now tracks the species' stages, we no longer require
separate stage subclasses for the pokemon_species class. 

Add html template variables to a get_html method in the  pokemon_species class 
and remove the sub classes that now have no methods or attributes of their own. 

Add a new html template variable for baby pokemon pages. (Previous code did not
include the baby stage of Pokemon evolution.))

3. Normalize the database to reflect the new class structure:
    
The ORM_object class relies on the table names in the database being the same
as the class names and the column headings in the tables being the same as the
data attributes. 
    
Write two new database tables with names identical to our pokemon_species and
pokemon_family classes. 
We will use our class names to access the tables. 

The pokemon_species table has columns for UID, family, name and count 
and the pokemon_family table has columns for UID (a family ID distinct from
the UID of the individual pokemon species), candies, baby, first_stage, 
second_stage and third_stage. These column names are identical to our class data
attributes.  

The family column in the pokemon_species table contains a family UID that is
a foreign key. The pokemon stages columns in the pokemon_family table 
have foreign key constraints to individual species' UIDs in the pokemon_species 
table.    
"""

# Importlib needed in order to import mysql.connector
# Spyder gives a 'not used' alarm because it doesn't know it's being used 
# behind the scenes

import http.server
import socketserver
import importlib
import mysql.connector

PORT = 80

# Because our ORM code is generic, we assign the database variable outside of 
# the ORM_object class

database_name = 'Pokemon'

"""
The ORM_object class handles all database operations. It is the interface 
between our application code and the database. We assume our user defined 
types (classes) have identical table names in the database so that all our
object attribute values can be stored to and loaded from the database with 
generic code. 

The __init__ method instantiates objects, assigning our table column headings 
to data attribute names. This is an abstract process that will not change 
if new classes with unique data attributes are added to the application code. 
Data attribute values stored in table rows are loaded using each 
object's unique ID.
 
The store method updates table data with attribute values using the object's 
UID to find the relevant table row.
  
Cross references between database tables using foreign keys could lead to 
multiple loads of one object. To avoid this the ORM_object class keeps an 
ID_to_object dictionary that guarantees an object is loaded only once per 
interpreter session. The value_to_ORM_object helper function fetches objects
from the dictionary and calls the ORM_object class to instantiate new objects. 
"""

class ORM_object(object):
    """
    Loads a database object from specified table
    Stores data attributes to relevant table
    """
    # Class variable dict maps object values to IDs
    # This prevents creating multiple objects for the same ID
    ID_to_object = {}
    
    # The init method constructs the database object 
    def __init__(self, ID):
        """
        Retrieves column headings from the database table 
        Sets object data attribute names with column headings
        Selects stored object values from table
        Sets object attribute values
        """
        # The class name must be identical to the table name
        self.table = self.__class__.__name__
        
        # Add the object to the class dictionary (this must be done before 
        # loading the data attribute values otherwise the foreign keys will 
        # cause multiple loads
        
        # Keys are a tuple (table_name, UID), because UIDs are not global 
        # (different tables in the database may use the same UID for a row)
        ORM_object.ID_to_object[(self.table, ID)] = self
        
        # Create a connection to the mysql server
        # These are the default login details
        # Port 8889 is the port MAMP uses to connect to MySQL
        # This recreates the connection on every load, which is inefficient but 
        # OK for now
        cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1', port="8889",
                                  database = database_name)
        
        # We have no multi statement transactions, so it's fine to use 
        # autocommit
        cnx.autocommit = True 
        # Create a cursor object
        cursor = cnx.cursor()
        # Get the column names from the table
        cursor.execute("SELECT * from " + self.table + " LIMIT 1")
        self.columns = cursor.column_names
        # Clear the cursor so it's willing to read again
        cursor.fetchone()
        
        # In case of a column being a foreign key we need to substitute the
        # object for the ID:
       
        # Get a list of foreign keys for this table
        # All our tables have a UID primary key column. A foreign key in one 
        # table is always a UID in another one
        cursor.execute("SELECT COLUMN_NAME, REFERENCED_TABLE_NAME from\
                       information_schema.KEY_COLUMN_USAGE WHERE\
                       CONSTRAINT_SCHEMA = '" + database_name + "'\
                       AND TABLE_NAME = '" + self.table + "'\
                       AND REFERENCED_COLUMN_NAME = 'UID'")
        keys_and_tables = cursor.fetchall()
        
        # Store foreign keys as dictionary keys with their referenced tables for 
        # values
        foreign_keys = {}
        
        for pair in keys_and_tables:
            foreign_keys[pair[0]] = pair[1]
            
        # load the row for this UID
        cursor.execute("SELECT * FROM " + self.table + " WHERE UID = " + str(ID))
        
        # a list with a tuple containing the values as its first element:
        data_for_attribute_values = cursor.fetchall()
        
        index = 0

        # This loop sets data attribute names for the object and assigns
        # values to them
        for column_name in self.columns:
        
            attribute_value = data_for_attribute_values[0][index]
                
            # First check if the value is a foreign key
            # If it is get the object with the foreign key UID
            if column_name in foreign_keys and attribute_value != None:
                referenced_table = foreign_keys[column_name]
                try:
                    fk_object = ORM_object.ID_to_object[(referenced_table, attribute_value)]
                # If the object is not already saved to the ORM_object class 
                # dictionary:
                except KeyError:
                    # Get the class object using the table name
                    _class = globals()[referenced_table]
                    # Load a new object
                    fk_object = _class(attribute_value)  
                    
                # Make data attribute name from the column name and assign the 
                # value. eg: the attribute self.UID is made from column name 'UID' 
                # and assigned UID value from the table           
                finally:
                    setattr(self, column_name, fk_object)
            
            else:
                setattr(self, column_name, attribute_value)
                
            index += 1

        # Close the cursor and connection to tidy up
        cursor.close()
        cnx.close()
        
    def store(self):
        """
        Stores data attribute values to database
        """
        # Create a connection to the mysql server
        cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1', port="8889",
                                  database = database_name)
        
        cursor = cnx.cursor()
        
        # We have no multi statement transactions, so it's fine to use 
        # autocommit
        cnx.autocommit = True
        
        SQL = "UPDATE " + self.table + " SET "
        
        first_column = True
        for column_name in self.columns:
            # get the data attribute value 
            attribute_value = getattr(self, column_name) 
            
            if attribute_value == None:
                attribute_value = 'NULL'
                
            elif isinstance(attribute_value, ORM_object):
                attribute_value = attribute_value.UID
            
            # SQL must have ' around text values but not ints
            if type(attribute_value) == str and attribute_value != 'NULL':
                attribute_value = "'" + attribute_value + "'"
         
            if not first_column:
                SQL += ", "
                
            SQL += "`" + column_name + "` = " + str(attribute_value)
            first_column = False
        
        SQL += " WHERE `UID` = " + str(self.UID) + ";"
        
        cursor.execute(SQL)
      
        # Close the cursor and database to tidy up
        cursor.close()
        cnx.close()

# The value_to_ORM_object function is the main interface between the application
# code and the ORM. The application code does not use UIDs, these are internal
# to the ORM. The application code identifies an object using a unique data 
# attribute which it supplies here. 
# This function gets the UID using the supplied data attribute name and returns 
# the object for that UID. 
# Class data attributes match database table column names exactly
        
def value_to_ORM_object(class_name, attribute_name, value):
    """
    class_name, attribute_name and value are all strings
    Attribute name is equal to column name in table
    Selects UID from the table row where the value matches the given column
    name
    Retrieves ORM_object from class dictionary using UID or calls ORM_object 
    class to instantiate a new object
    """
    assert type(class_name)==str and type(attribute_name)==str and type(value)==str
    
    cnx = mysql.connector.connect(user='root', password='root',
                              host='127.0.0.1', port="8889",
                              database = database_name)
    
    cursor = cnx.cursor()
    cursor.execute("SELECT UID FROM " + class_name + " WHERE `" 
                   + attribute_name + "` = '" + value + "';" )
    UID = cursor.fetchone()[0]
    
    if (class_name, UID) not in ORM_object.ID_to_object:
        _class = globals()[class_name]
        new_object = _class(UID)
        ORM_object.ID_to_object[(class_name, UID)] = new_object
        
    cursor.close()
    cnx.close()
        
    return ORM_object.ID_to_object[(class_name, UID)]


# End of object relational map to database. 
# Our application code starts here. 
            
class pokemon_family(ORM_object):
    """
    Keeps track of family pokemon stages and candies per family
    """
  
    def set_candies(self, candies):
        """
        candies, a positive integer
        """
        assert type(candies) == int
        self.candies = candies
        self.store()
    
       
class pokemon_species(ORM_object):
    """
    pokemon_species data attributes are used to construct the body of a web 
    page representing that species
    keeps track of species counts
    """
    # The class needs a specialized init procedure because the status line 
    # is not stored in the database. It must be instantiated here.
    def __init__(self, ID): 
        ORM_object.__init__(self, ID)
        
        self.status_line = ""
        
    def set_pokemon_count(self, new_count):
        """
        New_count is an int
        Updates Pokemon count and saves to database
        """
        assert type(new_count) == int
        self.count = new_count
        self.store()
    
    def template_substitute(self, template):
        """
        Takes an html string template and substitutes values for variables.
        Returns html string
        """
        # If the number of $ is not even, raise an error; template format wrong. 
        assert template.count('$')%2 == 0 
            
        # List of strings; every second string represents a variable requiring 
        # value substitution 
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
                # call helper function here, it will return the value of the 
                # attribute 
                new_value = attribute_value_for_template(self, 
                                                        template_segments[index])
                
                if isinstance(new_value, int):
                    new_value = str(new_value)
                    
                if not isinstance(new_value, str):
                    raise TypeError
    
                html += new_value
                    
            index += 1
    
        return html

    # get_html method is updatated to reflect our new class structure   
    def get_html(self):
        """
        Identifies the stage of pokemon_species using the pokemon_family 
        class attributes
        Returns html variable for the stage
        """
                
        if self == self.family.first_stage:
            html = self.template_substitute('''
<h1>$name$</h1>
$status_line$
<p>$name$ is a first stage Pokemon.</p>
<p>$name$ evolves into a <a href = "/$family.second_stage.name$">$family.second_stage.name$</a></p>
<p>Its third stage is a <a href = "/$family.third_stage.name$">$family.third_stage.name$</a></p>

<form action="$name$" method="post">
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0"> $name$s
    and
    <input type="number" name="new_candies" value = "$family.candies$" min="0"> $name$ candies.
  </p>
  <button type="submit">Update</button>
</form>
''')
    
        elif self.family.second_stage != None and self == self.family.second_stage:
            html = self.template_substitute('''
<h1>$name$</h1>
$status_line$
<p>$name$ is a second stage Pokemon.</p> 
<p>$name$ evolves from a <a href = "/$family.first_stage.name$">$family.first_stage.name$</a></p> 
<p>Its third stage is a <a href = "/$family.third_stage.name$">$family.third_stage.name$</a><br></p> 
<p>$name$ uses <a href = "/$family.first_stage.name$">$family.first_stage.name$</a> candies. You have $family.candies$ of them.<br></p> 

<form action="$name$" method="post">                     
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0"> $name$s
  </p>
  <button type="submit">Update</button>
</form>
''')   
        
        elif self.family.third_stage != None and self == self.family.third_stage:
            html = self.template_substitute('''
<h1>$name$</h1>
$status_line$
<p>$name$ is a third stage Pokemon.</p>
<p>$name$ evolves from a <a href = "/$family.second_stage.name$">$family.second_stage.name$</a></p>
<p>Its first stage is a <a href = "/$family.first_stage.name$">$family.first_stage.name$</a></p>
<p>$name$ uses <a href = "/$family.first_stage.name$">$family.first_stage.name$</a> candies. You have $family.candies$ of them.</p>

<form action="$name$" method="post">                     
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0"> $name$s
  </p>
  <button type="submit">Update</button>
</form>
''')
        
        elif self.family.baby != None and self == self.family.baby:
            html = self.template_substitute('''
<h1>$name$</h1>
$status_line$
<p>$name$ is a baby Pokemon.</p>
<p>$name$ evolves into a <a href = "/$family.first_stage.name$">$family.first_stage.name$</a></p>
<p>Its second stage is a <a href = "/$family.second_stage.name$">$family.second_stage.name$</a></p>
<p>Its third stage is a <a href = "/$family.third_stage.name$">$family.third_stage.name$</a></p>

<form action="$name$" method="post">
  <p>You have 
    <input type="number" name="new_count" value = "$count$" min="0"> $name$s
    and
    <input type="number" name="new_candies" value = "$family.candies$" min="0"> $name$ candies.
  </p>
  <button type="submit">Update</button>
</form>
''')  
        else:
            raise AttributeError ("Problem identifying pokemon species stage.") 
          
        return html
    
    
# Helper function for template_substitute method
def attribute_value_for_template(_instance, index):
    """
    index is a string of attributes separated by dots
    """
    attributes = index.split('.')
    next_instance = getattr(_instance, attributes[0])
    
    # Temporary kludge: we need branches in our template engine
    # Not all families have all stages of pokemon species
    if next_instance == None:
        next_instance = 'None at this time, also do NOT click here.'
        return next_instance
    
    attributes = attributes[1:]
    
    if attributes == []:
        return next_instance
    else: 
        attributes = '.'.join(attributes)
        return attribute_value_for_template(next_instance, attributes)
    

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

    # Pokemon_dictionary, in previous versions, is now replaced by database

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
        page_name = path[1:]         # strip the leading slash
      
        # send css
        if page_name == "pokemon_page.css":
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/css')
            self.end_headers()
            html = '''.status_line {
              margin:30px;
              border:2px solid #006600;
              padding:10px;
              font-family:Constantia,Georgia,"Times New Roman","Times Roman", Times,TimesNR,serif;
              font-size:25px;
              color:#006600; 
              text-align:center; 
              background-color:#dbffb6; 
              width:450px;
             }
            h1 {
              font-family:Constantia,Georgia,"Times New Roman","Times Roman",
              Times,TimesNR,serif;
              font-size:40px; font-style:italic;
            }
            input {
              width:50px;
            }'''
            self.wfile.write(html.encode('utf-8')) 
        
        # if the path is the name of a known pokemon, get its html string and 
        # construct the response:
        else:
            try:
                loaded = value_to_ORM_object('pokemon_species', 'Name', 
                                             page_name)
                self.send_response(http.HTTPStatus.OK)
                self.send_header("Content-type", 'text/html')
                self.end_headers()
                html = self.boilerplate_prefix + loaded.get_html() + self.boilerplate_suffix
                self.wfile.write(html.encode('utf-8')) 
              
            except:
                self.send_error(http.HTTPStatus.NOT_FOUND, "Pokemon species not found.".format(self.path))

    # Source code for the HTTPRequestHandler class: 
    # https://github.com/python/cpython/blob/2.7/Lib/BaseHTTPServer.py
    # "  - rfile is a file object open for reading positioned at the start of 
    # the optional input data part "
                
    # Python documentation for working with streams: 
    # https://docs.python.org/3/library/io.html

    def do_POST(self):
        
        '''
        Processes a POST request to update the count of pokemons and/or candies 
        of a species
        '''
        path = self.path
        page_name = path[1:]    # strip leading slash
        
        # self.rfile is the data string. It's an io.BufferedReader object 
        # (a binary object).
        # io.BufferedReader has a read method that requires a length argument.
        # self.headers gets the http headers as a dict. Content-Length is one 
        # of the headers, a dict key, the length of the data string. 
        # All header values are strings, so we coerce it to an int.
        # The read method returns a python bytes object, not a python string, 
        # so we have to convert it using the decode method.
        
        user_update = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        
        parsed = self.parse_http_arguments(user_update)
        
        # Update data in the pokemon class
        try:
            loaded = value_to_ORM_object('pokemon_species', 'Name', page_name)
            
            if 'new_candies' in parsed:
                loaded.family.set_candies(int(parsed['new_candies']))
                            
            # Every update sets the count, whereas only first-stage updates 
            # set the candies
            loaded.set_pokemon_count(int(parsed['new_count']))
            loaded.status_line = '''<p class="status_line">Updated</p>'''
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-type", 'text/html')
            self.end_headers()
            html = (self.boilerplate_prefix + loaded.get_html() + self.boilerplate_suffix)
            self.wfile.write(html.encode('utf-8')) 
            
            # Clear the status line so that it does not show as
            # updated in subsequent GET requests
            loaded.status_line = ""
                
        # 404 error: load method failed
        except:
            self.send_error(http.HTTPStatus.NOT_FOUND, \
                            "Could not set candies for this Pokemon family.".format(self.path))

# set up an OS connection at PORT 80, specify the handler for the port, wait for a url request 
with socketserver.TCPServer(("", PORT), PokemonHandler) as httpd:
   print("serving at port", PORT)
   # an infinite loop of waiting for a request
   httpd.serve_forever()

        
        
