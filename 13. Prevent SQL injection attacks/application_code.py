#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:33:07 2019

@author: ElAwbery
"""

"""
Application_code module constructs the web page view. 

Application code consists of two ORM_object subclasses, pokemon_family and 
pokemon_species.

The pokemon_family subclass keeps track of candy counts and family members 
which are pokemon_species objects. 

The pokemon_species subclass keeps track of individual pokemon counts. 

The Pokemon database mirrors the subclass structure with two tables. 
    
The pokemon_species subclass has data attributes UID, family, name and count 
and the pokemon_family subclass has data attributes UID (a family ID distinct from
the UID of the individual pokemon species), candies, baby, first_stage, 
second_stage and third_stage. 

The ORM_object class relies on table names in the database being identical to
its subclass names and the column headings in the tables being identical to the
subclass data attributes.

Thus our subclass data attributes are identical to our database table 
column names.

The family column in the pokemon_species table contains a family UID that is
a foreign key. The pokemon stages columns in the pokemon_family table 
have foreign key constraints to individual species' UIDs in the pokemon_species 
table.   

Our application code has been updated to call the server and talk to it with an 
HTTPRequestHandler subclass,'pokemon_handler'. Its get_router and post_router 
methods handle application specific page construction. These constitute the
controller of the MVC architecture.
"""

import database_ORM as ORM
import server
import template


class pokemon_family(ORM.ORM_object):
    """
    Keeps track of family pokemon stages and candies per family
    """
       
              
class pokemon_species(ORM.ORM_object):
    """
    pokemon_species data attributes are used to construct the body of a web 
    page representing that species
    keeps track of species counts
    """  
    
    def __init__(self, ID): 
        ORM.ORM_object.__init__(self, ID)
        self.status_line = ""      
    
    def get_html(self):
        """
        Identifies the stage of pokemon_species using the pokemon_family 
        class attributes
        Returns html variable for the stage
        """
             
        # Every family has a first stage, so we don't need to null-check here
        if self == self.family.first_stage:
            html = template.substitute(self, '''
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
            html = template.substitute(self, '''
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
            html = template.substitute(self, '''
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
            html = template.substitute(self, '''
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


class pokemon_handler(server.applicationHandler):
    """
    Handles application-specific web page construction and user actions
    get_router and post_router methods tell the server how to deal with requests
    """

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
    
    def get_router(self):
        """
        Generates a GET request response, e.g. from html boilerplate plus species-specific html.
        Returns a tuple, content_type (eg: html or css) and contents.
        If url not found, returns string for 404 error message. 
        """
        path = self.path
        page_name = path[1:]         # strip the leading slash
      
        # Response for CSS request
        if page_name == "pokemon_page.css":
            
            content_type = 'text/css'
            
            contents = '''.status_line {
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
            
        # if the path is the name of a known pokemon, get its html string and 
        # construct the response:
        else:
            try:
                loaded = ORM.value_to_ORM_object('pokemon_species', 'Name', page_name)
                content_type = "text/html"
                contents = self.boilerplate_prefix + loaded.get_html() + self.boilerplate_suffix
              
            except:
                content_type = "error"
                contents = "Pokemon species not found."
                
        return (content_type, contents)

    def post_router(self):
        
        '''
        Processes a POST request to update the count of pokemons and/or candies 
        of a species.
        Returns a success page.
        '''
        path = self.path
        page_name = path[1:]    # strip leading slash
        arguments = self.arguments
        
        # Update data in the pokemon class
        try:
            
            loaded = ORM.value_to_ORM_object('pokemon_species', 'Name', page_name)
            
            if "new_candies" in arguments:

                loaded.family.candies = int(arguments["new_candies"])
                            
            # Every update sets the count, whereas only first-stage updates 
            # set the candies
            loaded.count = (int(arguments["new_count"]))
            loaded.status_line = '''<p class="status_line">Updated</p>'''
            content_type = "text/html"
            contents = self.boilerplate_prefix + loaded.get_html() + self.boilerplate_suffix
            
            # Clear the status line so that it does not show as
            # updated in subsequent GET requests
            loaded.status_line = ""
                
        # 404 error: load method failed
        except:
            content_type = "error"
            contents = "Could not set candies for this Pokemon family."
            
        return (content_type, contents)
 
# Call the server to run our application       
server.web_server(pokemon_handler)
