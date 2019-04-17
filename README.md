# Motivation

Lucky Egg is a self-orchestrated project in which I build a web framework from scratch in order to understand the principles of web development from the ground up. My learning style is unusual in that I want to understand the principles with which I am working. Although the final product will be an app that could be easily made with a modern web framework, my intention is not simply to make an app, but to fully understand how each component of the web architecture functions and how it contributes to the finished product. 

This approach would be inefficient if my purpose was simply to build a web site. It is usual and sometimes necessary to accept complex tools as given: many people build good sites using code they don't fully understand. My purpose here is to understand how web development works systematically, not to learn tools to make products. 

Prior to starting this project in December 2018 I had no web development experience other than occasionally writing a few lines of html. I started to learn Python in March 2018. After teaching myself the basic syntax (see my Python [practice repo](https://github.com/elawbery/Python-Practice)) I completed the EdX MIT 6.00.1x online [Introduction to Computer Science and programming](https://github.com/elawbery/MIT-6.00.1x) and 6.00.2x [Introduction to computational thinking and data science](https://github.com/ElAwbery/MIT-6.00.2x).

Eventually I intend to make a tutorial accompanying this project to facilitate others through the same learning process. Each of the steps in building the architecture will expand into a blog post in which I outline the next phase of the project and set a series of coding tasks for users to complete. 


# Building the framework

I started at a level just above a raw socket connection, using the SimpleHTTPrequestHandler from the Python server library. This parses the http request at the http protocol level. From there I have been building the web site and architecture in stages. I outline each completed stage below with a link to an updated version of the code. 

Once I've built each next component of the web framework, I replace it with an off-the-shelf component – one whose principles and function I then understand. For example: I implemented a simple template engine so that I knew how a template engine works and its role in the overall architecture. Then I replaced it with Jinja2. Duplicating all the functionality of Jinja2 was Thisunecessary because the point of the project is to understand in practice the structure of web frameworks and their internal dependencies. 


# The Pokemon Go Lucky Egg preparation app

The end product will be a web app for Pokemon Go players. Players can set off a Lucky Egg timer which lasts for 30 minutes. While the Lucky Egg is activated, they accomplish a set of tasks. Figuring out the tasks in real time takes longer than the 30 minutes so players normally prepare beforehand to get the best value from their Lucky Egg. 

My app will put together a paper sheet users can take into the field with them when they play Pokemon Go so they can tick off what needs to be done. 

One of the main tasks accomplished during a Lucky Egg timer is species' evolution. Pokemon species belong to families. A baby evolves into a first stage species, first stage to second stage, second to third. Not all species evolve, not all families have babies or second or third stages. Those species that do evolve require accumulation of a specified number of candies in order to do so. Different species need different amounts of their candy in order to evolve. Candies are the same across families: for example, a Squirtle is a first-stage Pokemon. Squirtle evolves into its second-stage, a Wartortle. Wartortle evolves into Blastoise. All of them use Squirtle candies.  

Normally players prepare for a Lucky Egg by looking through their Pokemon deck at their species counts and candies and working out which of their species they want to evolve. It can get confusing keeping track of candies and which species are ready to evolve: in the Pokemon Go app, Pokemon species are not ordered by family, so deciding whether or not to evolve a first stage or a second stage species, or whether to wait for more candies, may involve scrolling back and forth many times through several hundred species.

My app will make it easy to see which species belong together in a Pokemon family. The to-do list is compiled based on calculations derived from information that the user enters manually from their Pokemon Go phone app into the Lucky Egg web app. Given user input data, the app will outline all possible evolutions and tasks for the Lucky Egg and will ask for user input again where they have a choice. The web app then makes a pdf that the user can print.

 
# System architecture
 
The web app is not yet finished. The end product will be a data entry app, with some options and a final button to press to produce the pdf. The system architecture on the back end is Flask-like. On the front end I'm planning to write some custom JavaScript to make sure I know how to do that, then to replace it with React. Finally I'll add the pdf generation functionality.

Below is a short summary of each step in the project. Each step involves the addition of some new functionality, or a significant refactoring. The section headers link to the finished version of my code for that step. Eventually I will present each of these steps in a tutorial page for other learners who want to understand web development in terms of the principle and function of its parts.  

<br>

## Bricks and mortar: building each block of the web framework  
 
### 1. Python talks to the browser

2. Made a web server 

3. Created a simple website in order to check that the server could handle requests for specified pages
    - Modified the server code to make a three page website
    - Each of the three pages contains different text; each page has its own url 
    - Each page contains links to the other two pages
    -up Added 404 error response to the handler
  
4. Refactored the code to make page object classes separate from the server code

5. Wrote an HTML form for user data entry

6. Added web forms to the page class

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



