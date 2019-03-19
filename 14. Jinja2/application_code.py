#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:33:07 2019

@author: Charlie
"""

"""
This version of the application code discards our home-built template engine 
and imports jinja2 in its place. 

A base template .html file with four child templates for pokemon species stages 
replace the html variables in the get_html method in previous versions. 

jinja2 supports conditionals, needed to handle missing family stages. I decided
not to add that functionality to my simple template engine, to avoid reinventing
the wheel. jinja2 also has loops, which we'll use later to create a new HTML
table view showing all Pokemon in all familes in a single screen. 
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

from jinja2 import FileSystemLoader, Environment

def render_template(_template, pokemon):
    """
    Renders the given template for the given pokemon
    """
    # The template conditionally includes HTML for stages that might be missing;
    # we pass species names into the template, and None for missing ones.
    if pokemon.family.baby == None:
        baby = None
    else:
        baby = pokemon.family.baby.name
    
    if pokemon.family.second_stage == None:
        second = None
    else:
        second = pokemon.family.second_stage.name
        
    if pokemon.family.third_stage == None:
        third = None
    else:
        third = pokemon.family.third_stage.name
    
    # FileSystemLoader loads the .html templates from the template directory
    loader = FileSystemLoader("Pokemon_templates")
    # Load the environment
    env = Environment(loader=loader)
    # Load the requested template
    template = env.get_template(_template)
    # pass variable-value pairs to render the template 
    return template.render(baby = baby,
                            first = pokemon.family.first_stage.name,
                            second = second, 
                            third = third, 
                            name = pokemon.name,
                            status_line = pokemon.status_line,
                            count = pokemon.count, 
                            candies = pokemon.family.candies)

class pokemon_family(ORM.ORM_object):
    """
    Keeps track of family pokemon stages and candies per family
    """
       
              
class pokemon_species(ORM.ORM_object):
    """
    pokemon_species data attributes are used to construct the body of a web 
    page representing that species.
    Keeps track of species counts.
    """
    
    def __init__(self, ID): 
        ORM.ORM_object.__init__(self, ID)
        self.status_line = ""
        
    def get_html(self):
        """
        Identifies the stage of pokemon_species using the pokemon_family 
        class attributes.
        Returns html variable for the stage.
        """
             
        # Every family has a first stage, so we don't need to null-check here
        if self == self.family.first_stage:
            html = render_template('first_stage.html', self)
            
        elif self.family.second_stage != None and self == self.family.second_stage:
            html = render_template('second_stage.html', self)
            
        elif self.family.third_stage != None and self == self.family.third_stage:
            html = render_template('third_stage.html', self)
           
        elif self.family.baby != None and self == self.family.baby:
            html = render_template('baby.html', self)

        else:
            raise AttributeError ("Problem identifying pokemon species stage.") 
          
        return html


class pokemon_handler(server.applicationHandler):
    """
    Handles application-specific web page construction and user actions.
    get_router and post_router methods tell the server how to deal with requests.
    """
    # HTML page boilerplate in previous versions is now saved as .html base template

    def get_router(self):
        """
        Generates a GET request response, e.g. from rendered .html templates.
        Returns a tuple, content_type (e.g.: html or css) and contents.
        If url not found, returns string for 404 error message. 
        """
        path = self.path
        # strip the leading slash
        page_name = path[1:]         
      
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
            }
            .container {
                margin: 1em;
            }'''
            
        # if the path is the name of a known pokemon, get its html string and 
        # construct the response:
        else:
            try:
                loaded = ORM.value_to_ORM_object('pokemon_species', 'Name', page_name)
                content_type = "text/html"
                contents = loaded.get_html() 
              
            except:
                content_type = "error"
                contents = "Pokemon species not found."
                
        return (content_type, contents)


    def post_router(self):
        
        """
        Processes a POST request to update the count of pokemons and/or candies 
        of a species.
        Returns a success page.
        """
        path = self.path
        # strip leading slash
        page_name = path[1:]    
        # arguments is a variable inherited from superclass
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
            contents = loaded.get_html()
            
            # Clear the status line so that it does not show as
            # updated in subsequent GET requests
            loaded.status_line = ""
                
        # 404 error: load method failed
        except:
            content_type = "error"
            contents = "Update failed."
            
        return (content_type, contents)
 
# Call the server to run the application       
server.web_server(pokemon_handler)