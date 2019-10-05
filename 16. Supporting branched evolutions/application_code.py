#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:33:07 2019

@author: ElAwbery
"""

"""
Application_code module constructs the web page view. 

This version updates the class structure to handle multiple evolution options.
For example, first stage Pokemon Eevee can evolve into one of several second 
stages such as Volteon, Vaporeon, Umbreon. 

This application code merges the two ORM_object subclasses in previous versions, 
pokemon_family and pokemon_species, into a single subclass: pokemon_species.

The application code must comply with the database ORM. Thus the Pokemon database 
now mirrors the subclass structure with one table in place of its previous two.

The ORM_object class relies on table names in the database being identical to
its subclass names and the column headings in the tables being identical to the
subclass data attributes.

Subclass data attributes (table column names) in this version are stage, 
family_candies, count and evolution requirements: candy_to_evolve and item_to_evolve. 
Every pokemon now has a first_stage attribute which 
identifies its evolution chain (previously 'family'). This column in the database 
has a foreign key constraint, enforcing a link with an object in the table. 
The first_stage attribute value of a first stage pokemon is itself. 

The function add_stages_to_first_stage keeps track of evolution paths, including
multiple branching. It assigns second stage and third stage data attributes to 
first stage pokemon objects. These attributes are lists of
species objects. Unlike in previous versions these attributes are handled by 
the application code and are not saved to the database.  
Second and third stage pokemon keep track of their evolution chain via their 
first_stage attribute.  

Our application code calls the server and talks to it with an 
HTTPRequestHandler subclass,'pokemon_handler'. Its get_router and post_router 
methods handle application specific page construction. These constitute the
controller of the MVC architecture.
"""


"""
The render_template function of the previous version is updated to account for 
second and third stage attributes (lists of pokeomon objects).
"""

import database_ORM as ORM
import server

from jinja2 import FileSystemLoader, Environment

def render_template(_template, pokemon = None, status_line = None):
    """
    Renders the given template for the given pokemon
    pokemon is None by default in case of AllPokemon page view which does not 
    need a pokemon species argument.
    """
    
    # FileSystemLoader loads the .html templates from the template directory
    loader = FileSystemLoader("Pokemon_templates")
    
    # Load the environment
    env = Environment(loader=loader)
    
    # Load the requested template
    template = env.get_template(_template)
    
    if status_line == 'updated':
        status_line = '''<p class="status_line">Updated</p>'''
            
    else:
        status_line = ''
    
    # renders individual pokemon_species templates
    if pokemon != None:
        
        # The pokemon_species templates conditionally include HTML for stages that 
        # might be missing;
        # we pass species names into the template, and None for missing ones.
        second_stages = pokemon.first_stage.second_stages
        if second_stages == []:
            second = None
            second_evo_requirements = None
        else:
            second = []
            for species in second_stages:
                second.append(species.name)
                second_evo_requirements = str(species.candy_to_evolve)
            
        third_stages = pokemon.first_stage.third_stages
        if third_stages == []:
            third = None
            third_evo_requirements = None
        else:
            third = []
            for species in third_stages:
                third.append(species.name)
                third_evo_requirements = str(species.candy_to_evolve)
        
        # pass variable-value pairs to render the template
        return template.render(first = pokemon.first_stage.name,
                                second = second, 
                                third = third, 
                                name = pokemon.name,
                                count = pokemon.count, 
                                candies = pokemon.first_stage.family_candies,
                                second_evo_requirements = second_evo_requirements,
                                third_evo_requirements = third_evo_requirements,
                                status_line = status_line)
        
    # renders the AllPokemon template
    else:
        
        # An ordered list of all pokemon_species objects
        # We use this to render the template rather than the ORM ID_to_object 
        # dict itself because that also contains pokemon family objects.
        all_pokemon = ORM.all_objects_of_class('pokemon_species', 'name')
                     
        # a for loop in the template assigns pokemon_species' names to their 
        # count and candy updates
        return template.render(all_pokemon = all_pokemon, 
                               status_line = status_line)
               
              
class pokemon_species(ORM.ORM_object):
    """
    pokemon_species data attributes are used to construct the body of a web 
    page representing that species.
    Keeps track of species counts.
    """
    
    def __init__(self, ID): 
        ORM.ORM_object.__init__(self, ID)
        
        
    def get_html(self, status_line):
        """
        Identifies the stage of pokemon_species using the pokemon_family 
        class attributes.
        Returns html variable for the stage.
        """
        # Every family has a first stage, so we don't need to null-check here
        if self.stage == 1:
            html = render_template('first_stage.html', self, status_line)
            
        elif self.stage == 2:
            html = render_template('second_stage.html', self, status_line)
            
        elif self.stage == 3:
            html = render_template('third_stage.html', self, status_line)

        else:
            raise AttributeError ("Problem identifying pokemon species stage.") 
          
        return html


def add_stages_to_first_stage(first_stage_object):
    """
    Adds second_stages and third_stages attributes to first_stage pokemon
    """
    
    # All species access their evolution stages via their first_stage attribute
    # In the database the first_stage column has a foreign key constraint 
    # to the UID column

    # List of objects of all stages of this pokemon
    evolutions = ORM.all_objects_of_class('pokemon_species', 'first_stage', first_stage_object.UID)

    # Note: attributes second_stages and third_stages are not in the database
    # These attributes are lists, which make it possible to store multiple same stage evolutions, 
    # e.g. Evee has several second stage evolutions such as Vaporeon, Jolteon
    first_stage_object.second_stages = []
    first_stage_object.third_stages = []
    for species in evolutions:
        if species.stage == 2:
            first_stage_object.second_stages.append(species) 
        elif species.stage == 3:
            first_stage_object.third_stages.append(species)

# When this is False, we catch errors and return a 404. Otherwise, when
# debugging, we raise the error so we can see what went wrong.
DEBUG_POST = False

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
              
        # Response for CSS requests. 
        # TODO: put these in separate .css files
        if page_name == "pokemon_page.css":
            
            content_type = 'text/css'
            
            contents = '''.status_line {
              margin-top: 30px;
              margin-bottom: 30px;
              margin-left: 20px;
              border: 2px solid #006600;
              padding: 10px;
              font-family: Constantia,Georgia,"Times New Roman","Times Roman", Times,TimesNR,serif;
              font-size: 25px;
              color: #006600; 
              text-align: center; 
              background-color: #dbffb6; 
              width: 450px;
             }
            h1 {
              font-family: Constantia,Georgia,"Times New Roman","Times Roman",
              Times,TimesNR,serif;
              font-size: 40px; 
              font-style: italic;
              margin: 20px;
            }
            input {
              width: 50px;
            }
            button {
              font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif;
              height: 30px;
              width: 100px;
              font-size: 16px;
              border-radius: 10px;
              border: 1px solid green;
              margin-top: 20px;
              margin-bottom: 20px;
              background-color: white;
            }
            a {
              text-decoration: none;
            }
            a.button {
              font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; 
              border-radius:10px;
              border: 1px solid green;
              background-color: white;
              padding: 8px;
              color: black;
              text-align: center;
            }
            .container {
                margin: 20px;
            }'''
            
        elif page_name == "all_pokemon.css":

            content_type = 'text/css'

            contents = '''.status_line {
              margin: 30px;
              border: 2px solid #006600;
              padding: 10px;
              font-family: Constantia,Georgia,"Times New Roman","Times Roman", Times,TimesNR,serif;
              font-size: 25px;
              color: #006600; 
              text-align: center; 
              background-color: #dbffb6; 
              width: 450px;
             }
            table {
              border-collapse: collapse;
              margin: 30px;
              width: 450px;
              }
            table, th, td {
              border: 1px solid black; 
            }
            th, td {
              height: 25px;
              padding: 5px;
              text-align: left;
              vertical-align: bottom;
            }
            h1 {
              font-family: Constantia,Georgia,"Times New Roman","Times Roman",
              Times,TimesNR,serif;
              font-size: 40px; 
              font-style: italic;
              margin-left: 30px;
            }
            input {
              width: 75%;
            }
            button {
              height: 30px;
              width: 100px;
              font-size: 16px;
              border-radius: 10px;
              border: 1px solid green;
              background-color: white;
              margin: 30px;
            }
            a {
              text-decoration: none;
            }
            .container {
              margin: 2em;
            }'''
               
        elif page_name == 'AllPokemon':
            content_type = "text/html"
            contents = render_template('AllPokemon.html')
        
        # if the path is the name of a known pokemon, get its html string and 
        # construct the response:
        else:
            try:
                loaded = ORM.value_to_ORM_object('pokemon_species', 'name', page_name)
                add_stages_to_first_stage(loaded.first_stage)
                content_type = "text/html"
                contents = loaded.get_html(status_line = None) 
              
            except TypeError:
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
        
        # arguments is variable inherited from superclass, a dict containing
        # browser input in the form {'name_candies': int, 'name_count': int}
        arguments = self.arguments
        
        try:
            if page_name == "AllPokemon":                
              
                # for each pair in the arguments dict, load the object and 
                # update the candies or the count
                
                # keys take the form 'name_count' or 'name_candies'
                for key in arguments:
                    loaded = ORM.value_to_ORM_object('pokemon_species', 'name', key.split('_')[0])
                    # Update data in the pokemon class
                    if key.split('_')[1] == 'count':
                        loaded.count = arguments[key]
                    else:
                        loaded.first_stage.family_candies = arguments[key]
                
                content_type = "text/html"
                contents = render_template('AllPokemon.html', status_line = 'updated')

            else:
                loaded = ORM.value_to_ORM_object('pokemon_species', 'name', page_name)
                # Update data in the pokemon class
                if "new_candies" in arguments:
                    loaded.first_stage.family_candies = int(arguments["new_candies"])
                                
                # Every update sets the count, whereas only first-stage updates 
                # set the candies
                loaded.count = (int(arguments["new_count"]))
                content_type = "text/html"
                contents = loaded.get_html(status_line = 'updated')
                    
        # 404 error: load method failed
        except:
            if DEBUG_POST:
                raise
            else:
                content_type = "error"
                contents = "Update failed."
            
        return (content_type, contents)
 
# Call the server to run the application       
server.web_server(pokemon_handler)
