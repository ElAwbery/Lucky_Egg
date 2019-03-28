# Lucky_Egg
A full stack web development project

Incrementally builds a website starting at the lowest level of back end web development and working up from there. 

Each of the tasks below corresponds to the file with the same number. 

1. Established a connection with the browser 

2. Made a web server 

3. Created a simple website
    - Modified the server code to make a three page website
    - Each of the three pages contains different text; each page has its own url 
    - Each page contains links to the other two pages
    -up Added 404 error response to the handler
  
4. Separated pages from the server (created page objects)

5. Wrote an HTML form

6. Added web forms to the page classs

7. Added a POST method
    - Implemented the post method of the request handler class 
    - Client can now modify page class data attributes 
  
8. Wrote a template engine, added templates and template method to site 
    - Added templates to the HTML constructor in each stage class
    - Defined a template substitution method for the pokemon parent class 
    - Cleaned up the HTML 
  
9. Added CSS
    - Added header meta for CSS to HTML pages
    - Added code to server GET method to send CSS on request
    - Wrote simple CSS just to demonstrate that it works
    - Added status_line to HTML for "Updated", as a thing to apply CSS to
    (required minor restructuring of the HTML generation code)
    
10. Wrote load and save methods
     - Using MAMP with PHPMyAdmin set up a MySQL table
     - The SQL dump to make a MySQL table for the Python code to talk to is included here
     - Write Python methods to construct a Pokemon object from a row and save new data to the database using SQL strings
     
11. Refactoring code and normalizing the database:
    an exercise in separating the database operations from the application code. The ORM_object class has no code specific to        an application object type, and the application code must not know any information specific to the database. 

     - Wrote an object relational map to interface with the database
     - Refactored the class structure into two sub-classes of the ORM_object class
     - Normalized the database to reflect the new class structure
     
12. Modularization:

     - Organized the program into an MVC architecture containing four modules
     - The database_ORM expresses the model
     - Application_code module constructs the web page view
     - Application code updated to call the server and talk to it with an HTTPRequestHandler subclass
     - get_router and post_router methods of the Handler subclass constitute the controller of the MVC architecture
     - Server code is now separated from the application code into a server module
     - In principle the server can process any browser request and call the application's router methods
     - Web server no longer runs on loading, it is wrapped in a function called by application code
     - Template engine separated from the application module and contains no application specific code
     
13. Prevented SQL injection attacks and added store on set:

     - Added prepared cursor objects into the database_ORM and used parameters to update table values
     - Integrated set and store functionality into the ORM, replacing the store method of previous versions with a specialized setattr 
     - Updated application code so that it no longer sets attributes
     
14. Replaced home built template engine with Jinja2:

     - Added base template .html file with four child templates for pokemon species stages
     - Added function to render templates for pokemon species
     - Updated HTML variables in application code
     
15. Added tabular view:

     - Updated template rendering function to include a tabular page view of all pokemon species in all families
     - Added 'get all objects of a given class' functionality to ORM and separated UID_to_object method into a helper function
     - Added an all_pokemon css stylesheet to the pokemon handler class
     - Updated get_router and post_router request handling accordingly
     - Removed status line attribute from the pokemon class and made it a template variable instead

Thanks to [@meaningness](https://twitter.com/Meaningness) for advice on architectural design, and code review. 



