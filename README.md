# Motivation

Lucky Egg is a self-orchestrated project in which I build a web framework from scratch in order to understand the principles of web development from the ground up. My learning style is unusual in that I want to understand the principles with which I am working. Although the final product will be an app that could be easily made with a modern web framework, my intention is not simply to make an app, but to fully understand how each component of the web architecture functions and how it contributes to the finished product. 

This approach would be inefficient if my purpose was simply to build a web site. It is usual and sometimes necessary to accept complex tools as given: many people build good sites using code they don't fully understand. My purpose here is to understand how web development works systematically, not to learn tools to make products. 

Prior to starting this project in December 2018 I had no web development experience other than occasionally writing a few lines of html. I started to learn Python in March 2018. After teaching myself the basic syntax (see my Python [practice repo](https://github.com/elawbery/Python-Practice)) I completed the EdX MIT 6.00.1x online [Introduction to Computer Science and programming](https://github.com/elawbery/MIT-6.00.1x) and 6.00.2x [Introduction to computational thinking and data science](https://github.com/ElAwbery/MIT-6.00.2x).

Eventually I intend to make a tutorial accompanying this project to facilitate others through the same learning process. Each of the steps in building the architecture will expand into a blog post in which I outline the next phase of the project and set a series of coding tasks for users to complete.  
<br>
# Building the framework

I started at a level just above a raw socket connection, using the SimpleHTTPrequestHandler from the Python server library. This parses the http request at the http protocol level. From there I have been building the web site and architecture in stages. I outline each completed stage below with a link to an updated version of the code. 

Once I've built each next component of the web framework, I replace it with an off-the-shelf component – one whose principles and function I then understand. For example: I implemented a simple template engine so that I knew how a template engine works and its role in the overall architecture. Then I replaced it with Jinja2. Duplicating all the functionality of Jinja2 was Thisunecessary because the point of the project is to understand in practice the structure of web frameworks and their internal dependencies.  
<br>
# The Pokemon Go Lucky Egg preparation app

The end product will be a web app for Pokemon Go players. Players can set off a Lucky Egg timer which lasts for 30 minutes. While the Lucky Egg is activated, they accomplish a set of tasks. Figuring out the tasks in real time takes longer than the 30 minutes so players normally prepare beforehand to get the best value from their Lucky Egg. 

My app will put together a paper sheet users can take into the field with them when they play Pokemon Go so they can tick off what needs to be done. 

One of the main tasks accomplished during a Lucky Egg timer is species' evolution. Pokemon species belong to families. A baby evolves into a first stage species, first stage to second stage, second to third. Not all species evolve, not all families have babies or second or third stages. Those species that do evolve require accumulation of a specified number of candies in order to do so. Different species need different amounts of their candy in order to evolve. Candies are the same across families: for example, a Squirtle is a first-stage Pokemon. Squirtle evolves into its second-stage, a Wartortle. Wartortle evolves into Blastoise. All of them use Squirtle candies.  

Normally players prepare for a Lucky Egg by looking through their Pokemon deck at their species counts and candies and working out which of their species they want to evolve. It can get confusing keeping track of candies and which species are ready to evolve: in the Pokemon Go app, Pokemon species are not ordered by family, so deciding whether or not to evolve a first stage or a second stage species, or whether to wait for more candies, may involve scrolling back and forth many times through several hundred species.

My app will make it easy to see which species belong together in a Pokemon family. The to-do list is compiled based on calculations derived from information that the user enters manually from their Pokemon Go phone app into the Lucky Egg web app. Given user input data, the app will outline all possible evolutions and tasks for the Lucky Egg and will ask for user input again where they have a choice. The web app then makes a pdf that the user can print.  
<br>
# System architecture
 
The web app is not yet finished. The end product will be a data entry app, with some options and a final button to press to produce the pdf. The system architecture on the back end is Flask-like. On the front end I'm planning to write some custom JavaScript to make sure I know how to do that, then to replace it with React. Finally I'll add the pdf generation functionality.

Below is a short summary of each step in the project. Each step involves the addition of some new functionality, or a significant refactoring. The section headers link to the finished version of my code for that step. Eventually I will present each of these steps in a tutorial page for other learners who want to understand web development in terms of the principle and function of its parts.  
<br>
## Bricks and mortar: building each block of the web framework  
 
### 1. [Make a connection with the browser using Python](https://github.com/ElAwbery/Lucky_Egg/blob/master/01.%20Python_to_browser.py)
Write code to display the body of an html file in a browser tab. 

 - Write Python code to make an html file. This is stored locally. 
 - Import the Python os and webbrowser libraries. 

 The os.path module implements functions on pathnames. You can see the documentation here:
 https://docs.python.org/3/library/os.path.html

Use the os.path.abspath function to retrieve the full path to the stored html file.
Use the webbrowser.open_new_tab function to show our stored html page in the browser.  

I also wrote a couple of functions to take input from a user then make and store a new html file with the input. 


### 2. [Write a local web server to handle http requests](https://github.com/ElAwbery/Lucky_Egg/blob/master/02.%20Server.py)

Now we understand how to write to the browser from our code, we want to build a local server to do this for us, and to handle requests from the browser.

- Import the Python http.server and socketserver libraries. 

You can read the http.server documentation here: 
https://docs.python.org/3/library/http.server.html
 
- Rewrite the html code we wrote in Phase 1. Turn it into boilerplate variables for an html page. 
- Write a simple request handler using the built in MyHTTPRequestHandler class. The request handler should serve a GET request and construct an html page from the boilerplate variables and the path string.
- Set up a TCPsocketserver (transmission control protocol), specify the port to serve and tell it to use your handler.
 

### 3. [Make a three page website](https://github.com/ElAwbery/Lucky_Egg/blob/master/03.%20Three%20page%20website.py)

Make a simple website to test the server can handle unique page requests: 
 - Modify the request handler code to make a three page website. 
 - Each page has its own url and displays its own unique text. To do this you can set up a dictionary mapping the page path names to their content. 
 - Add links in the content for each page to both the other two pages.
 - Add a 404 error response to the request handler. If the browser asks for any page other than your three known page names, your code should return a 'page not found' response. 
  

### 4. [Separate out the website from the server code](https://github.com/ElAwbery/Lucky_Egg/blob/master/04.%20Page%20class.py)

Define a page class:
- The page class standardizes the formula for different types of web page.
- For the Lucky Egg app, the parent page class will be a pokemon object. For example, if Squirtle is a pokemon object, its web page will have the title 'Squirtle' and will tell the user about Squirtle. 
- The pokemon class will initialize name, first_stage, second_stage and third_stage attributes. 
- Write an update_candy_count method for the parent class and write a str method to retrieve the name of the pokemon object.

We need subclasses for different page types because each pokemon species stage has distinct characteristics. For example, we need a unique page formula for first_stage pokemon objects because only first_stage pokemon evolve into second stage pokemon: 
- Write three pokemon object subclasses: first_stage, second_stage and third_stage.
- Write an html_body method for each subclass. It returns the html string for the body of that page type.

All the pokemon species in one evolutionary sequence share the same candy, so only the first_stage pokemon object will keep track of the candy count.
- Initialize the candy_count attribute in the first_stage class.

Our GET request must be updated to get the correct html body for each page type:
- Change the pokemon dictionary keys from path strings to pokemon object names. Eventually we will map names to objects. 
- Re-write the pokemon dictionary values to call the required pokemon subclass html_body method.
- Finally, make sure all the code is well documented to reflect the changes.


### 5. [Write an HTML form for user data entry](https://github.com/ElAwbery/Lucky_Egg/blob/master/05.%20HTML%20form.py)

Read about HTML forms [here](https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Your_first_HTML_form) and [here](https://en.wikipedia.org/wiki/Form_(HTML)).

The Lucky Egg app user wants to know how many of a pokemon species they have, and how many of that pokemon family's candy. Eventually they want to update the species' count and the candy count.

- Write an HTML form with two input boxes for a pokemon species object, one box for that species' count (eg: how many Squirtles the user has in their pokemon app) and the other for its candy count.
- Add an update button.
- Integrate the form into the request handler class and test it displays correctly in the browser for its pokemon object page type.


### 6. [Add name_to_object method and web forms to the page class](https://github.com/ElAwbery/Lucky_Egg/blob/master/06.%20Add%20web%20forms.py)

Our pokemon dictionary values are becoming unwieldy. Now that we have an object oriented architecture, our class structure can keep track of all our user's pokemon data and turn it into HTML pages for the website incorporating our HTML forms. We need only refer to the pokemon object from outside the class. In order to do so, we want to be able to use our page name (the name of the pokemon species) from the browser to get all the required pokemon data:

- Re-write the pokemon dictionary so that its values are pokemon objects. It now maps pokemon names to objects. 
- Write a 'name_to_object' method for the pokemon class. It will retrieve the stored pokemon object from its string name in the pokemon dictionary.

We want the page type for each pokemon stage to display information about that pokemon's evolutionary sequence, how many the user has in their Pokemon app and how many candies they have for that sequence of evolutions:

- Add HTML forms to the 'html_body' methods for the pokemon stage subclasses.


### 7. [Add a POST method](https://github.com/ElAwbery/Lucky_Egg/blob/master/07.%20Write%20POST%20method.py)

We want to add functionality for the web app user to update their pokemon species' counts and candy counts. 
The Python documentation for working with streams is [here](https://docs.python.org/3/library/io.html).

- Implement the post method of the request handler class so that the client can modify class data attributes (pokemon species count and candy counts). 
- Catch errors with the built in 'send_error' method of Python's request handler class. 
- The updated pokemon species page should display its status as 'Updated'.  


### 8. [Write a template engine, add templates and a template method to the website code](https://github.com/ElAwbery/Lucky_Egg/blob/master/08.%20Add%20template%20to%20site.py)

The [wiki.Python page](https://wiki.python.org/moin/Templating) has information about template writing in Python. A general resource for understanding templating is [here](https://allwebcodesign.com/website-templates.htm). You should be familiar with the principle of substitution (eg: substituting values for variables, or actual parameters for formal parameters) before attempting this step.  

Here we will implement a simple templating system in order to understand how one works:
 - Write templates and add them to the HTML constructor in each stage class. Use data attribute names for variables.
 - Define the 'template_substitute' method for the pokemon parent class. This method takes an HTML string which is a template.
 - It substitutes values for variables into the template and returns the template string with substitutions. Use the Python 'getattr' method to get the required value for the variable.
 - What if your template string starts with a variable? Make sure you include code to cover for this eventuality.
 - The 'html_body' method in each stage class must return a template string complete with substitutions. It calls the 'template_substitute' method to get the finshed string.
 

### 9. [CSS implementation](https://github.com/ElAwbery/Lucky_Egg/blob/master/09.%20Add%20CSS.py)
    
We want the server GET method to send page CSS on request. The point of this exercise is to show that you can write CSS and understand how to add it into the application code. The HTML for each page will include a CSS page reference in its meta data which will generate a new GET request for the CSS. 

- Add a CSS page link to the header meta for HTML pages.
- Update the server GET method so that it will send the CSS page on request.
- Make some styling decisions and implement them as part of the CSS page. You could make the status line a class attribute, add it as a variable to the HTML template and apply CSS to make a colorful 'updated' banner.

    
  <br>
   <br>
    
10. Wrote load and save methods
     - Using MAMP with PHPMyAdmin set up a MySQL table
     - The SQL dump to make a MySQL table for the Python code to talk to is included here
     - Write Python methods to construct a Pokemon object from a row and save new data to the database using SQL strings
     
11. Refactoring code and normalizing the database:
    an exercise in separating the database operations from the application code. The ORM_object class has no code specific to        an application object type, and the application code must not know any information specific to the database. 

     - Wrote an object relational map to interface with the database
     - Refactored the application class structure into two sub-classes of the ORM_object class (species, family)
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



