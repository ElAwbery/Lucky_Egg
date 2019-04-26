# Motivation

Lucky Egg is a self-directed project in which I build a web framework from scratch in order to understand the principles of web development from the ground up. My learning style is unusual in that I want to understand the principles with which I am working. Although the final product will be an app that could be easily made with a modern web framework, my intention is not simply to make an app, but to fully understand how each component of the web architecture functions and how it contributes to the finished product. 

This approach would be inefficient if my purpose was simply to build a web site. It is usual and sometimes necessary to accept complex tools as given: many people build good sites using code they don't fully understand. My purpose here is to understand how web development works systematically, not to learn tools to make products. 

Prior to starting this project in December 2018 I had no web development experience other than occasionally writing a few lines of HTML. I started to learn Python in March 2018. After teaching myself the basic syntax (see my Python [practice repo](https://github.com/elawbery/Python-Practice)) I completed the EdX MIT 6.00.1x online [Introduction to Computer Science and programming](https://github.com/elawbery/MIT-6.00.1x) and 6.00.2x [Introduction to computational thinking and data science](https://github.com/ElAwbery/MIT-6.00.2x).

Eventually I intend to make a tutorial accompanying this project to facilitate others through the same learning process. Each of the steps in building the architecture will expand into a blog post in which I outline the next phase of the project and set a series of coding tasks for users to complete.  
<br>
# Building the framework

I started at a level just above a raw socket connection, using the SimpleHTTPrequestHandler from the Python server library. This parses the HTTP request at the HTTP protocol level. From there I have been building the web site and architecture in stages. I outline each completed stage below with a link to the corresponding version of the code. 

Once I've built each next component of the web framework, I replace it with an off-the-shelf component – one whose principles and function I then understand. For example: I implemented a simple template engine so that I knew how a template engine works and its role in the overall architecture. Then I replaced it with Jinja2. Duplicating all the functionality of Jinja2 was unecessary because the point of the project is to understand in practice the structure of web frameworks and their internal dependencies.  
<br>
# The Pokemon Go Lucky Egg preparation app

The end product will be a web app for Pokemon Go players. Players can set off a Lucky Egg timer which lasts for 30 minutes. While the Lucky Egg is activated, they accomplish a set of tasks. Figuring out the tasks in real time takes longer than the 30 minutes so players normally prepare beforehand to get the best value from their Lucky Egg. 

My app will generate a paper sheet (PDF) that users can take into the field with them when they play Pokemon Go so they can tick off what needs to be done. 

One of the main tasks accomplished during a Lucky Egg timer is species' evolution. Pokemon species belong to families. A baby evolves into a first stage species, first stage to second stage, second to third. Not all species evolve, not all families have babies or second or third stages. Those species that do evolve require accumulation of a specified number of candies in order to do so. Different species need different amounts of their candy in order to evolve. Candies are the same across families. For example, a Squirtle evolves into a Wartortle, which evolves into a Blastoise. All three species use Squirtle candies.  

Normally players prepare for a Lucky Egg by looking through their Pokemon deck at their species counts and candies and working out which of their species they want to evolve. It can get confusing keeping track of candies and which species are ready to evolve: in the Pokemon Go app, Pokemon species are not ordered by family, so deciding whether or not to evolve a first stage or a second stage species, or whether to wait for more candies, may involve scrolling back and forth many times through several hundred species.

My app will make it easy to see which species belong together in a Pokemon family. The to-do list is compiled based on calculations derived from information that the user enters manually from their Pokemon Go phone app into the Lucky Egg web app. Given user input data, the app will outline all possible evolutions and tasks for the Lucky Egg and will ask for user input again where they have a choice. The web app then makes a pdf that the user can print.  
<br>
# System architecture
 
The web app is not yet finished. The end product will be a data entry app, with some options and a final button to press to produce the pdf. The system architecture on the back end is Flask-like. On the front end I'm planning to write some custom JavaScript to make sure I know how to do that, then to replace it with React. Finally I'll add the pdf generation functionality.

Below is a short summary of each step in the project. Each step involves the addition of some new functionality, or a significant refactoring. The section headers link to the finished version of my code for that step. Eventually I will present each of these steps in a tutorial page for other learners who want to understand web development in terms of the principle and function of its parts.  
<br>
# Bricks and mortar: building each block of the web framework 

## Phase 1: building a simple web server and a website with object oriented programming
### 1. [Make a connection with the browser using Python](https://github.com/ElAwbery/Lucky_Egg/blob/master/01.%20Python_to_browser.py)

I wrote code to display the body of an HTML file in a browser tab. This was a preliminary exercise; the approach taken in the next stage was different, and none of this code carried over.

 - Wrote Python code to create an HTML file and write it to the file system. 
 - Imported the Python __os__ and __webbrowser__ libraries. 

 The os.path module implements functions on pathnames. The documentation is [here.](https://docs.python.org/3/library/os.path.html)

 - Used the os.path.abspath function to retrieve the full path to the stored HTML file.
 - Used the webbrowser.open_new_tab function to show the stored html page in the browser.

I also wrote a couple of functions to take input from a user then make and store a new HTML file incorporating the input. 


### 2. [Wrote a local web server to handle HTTP requests](https://github.com/ElAwbery/Lucky_Egg/blob/master/02.%20Server.py)

Once I understood how to write to the browser from my code, I wanted to build a local server to do this for me, and to handle requests from the browser.

- Imported the Python __http.server__ and __socketserver__ libraries. 

The http.server documentation is [here.](https://docs.python.org/3/library/http.server.html)
 
- Rewrote the HTML code from step 1. Turned it into boilerplate variables for an HTML page. 
- Wrote a simple request handler inheriting from the standard SimpleHTTPRequestHandler class. It serves a GET request and constructs an HTML page from the boilerplate variables and the path string.
- Set up a socket server, specifying the port to serve, and passed the handler class to it.
 

### 3. [Made a three page website](https://github.com/ElAwbery/Lucky_Egg/blob/master/03.%20Three%20page%20website.py)

Made a three-page website to test the server could handle page requests for different URLs, by modifying the request handler code: 
 - Each page has its own URL and displays its own unique text. To do this I set up a dictionary mapping the page path names to their content. 
 - Added HTML links in the content for each page to both the other two pages.
 - Added a 404 error response to the request handler. If the browser asks for any page other than the three known page names, the code returns a __page not found__ response. 
  

### 4. [Separated the specific website from the generic server code](https://github.com/ElAwbery/Lucky_Egg/blob/master/04.%20Page%20class.py)

Defined a page class:
- The page class standardizes the formula for different types of web page.
- For the Lucky Egg app, the parent page class is a pokemon object. For example, if Squirtle is a pokemon object, its web page will have the title 'Squirtle' and will tell the user about Squirtle. 
- The pokemon class initializes name, first_stage, second_stage and third_stage attributes. 
- Wrote an update_candy_count method for the parent class and  a __str__ method to retrieve the name of the pokemon object.

The class structure needed subclasses for different page types because each pokemon species stage has distinct characteristics. For example, it required a unique page formula for first_stage pokemon objects because only first_stage pokemon evolve into second stage pokemon: 
- Wrote three pokemon object subclasses: first_stage, second_stage and third_stage.
- Wrote an __html_body__ method for each subclass. It returns the HTML string for the body of that page type.

All the pokemon species in one family share the same candy, so only the first_stage pokemon object keeps track of the candy count.
- Initialized the candy_count attribute in the __first_stage__ class.

Updated the GET request to get the correct HTML body for each page type:
- Changed the pokemon dictionary keys from path strings to pokemon object names. (In step 6, I map names to objects.) 
- The pokemon dictionary values are created by calling the required pokemon subclass __html_body__ method.

### 5. [Wrote an HTML form for user data entry](https://github.com/ElAwbery/Lucky_Egg/blob/master/05.%20HTML%20form.py)

Read about HTML forms [here](https://developer.mozilla.org/en-US/docs/Learn/HTML/Forms/Your_first_HTML_form) and [here](https://en.wikipedia.org/wiki/Form_(HTML)).

The Lucky Egg app user wants to know how many of a pokemon species they have, and how many of that pokemon family's candy. Later I add functionality to update the species' count and the candy count; in this step I'm just generating the form.

- Wrote an HTML form with two input boxes for a pokemon species object, one box for that species' count (e.g.: how many Squirtles the user has) and the other for its candy count.
- Added an update button.
- Integrated the form into the request handler class and tested it displayed correctly in the browser for its pokemon object page type.


### 6. [Added name_to_object method and web forms to the page class](https://github.com/ElAwbery/Lucky_Egg/blob/master/06.%20Add%20web%20forms.py)

The pokemon dictionary values were becoming unwieldy. Now that I have an object oriented architecture, the class structure can keep track of all the user's pokemon data and turn it into HTML pages for the website using HTML forms. The code outside the class need only refer to the pokemon object. In order to implement that I wanted to use the URL (which is the name of the pokemon species) to get all the required pokemon data:

- Re-wrote the pokemon dictionary code so it maps pokemon names to objects (rather than HTML strings). 
- Wrote a __name_to_object__ method for the pokemon class. It retrieves the stored pokemon object from its string name in the pokemon dictionary.

I wanted the page type for each pokemon stage to display information about that pokemon's family (evolutionary sequence), how many instances of the species the user has in their Pokemon app, and how many candies they have for that family:

- Added HTML forms to the __html_body__ methods for the pokemon stage subclasses.


### 7. [Added a POST method](https://github.com/ElAwbery/Lucky_Egg/blob/master/07.%20Write%20POST%20method.py)

This step added functionality for the web app user to update their pokemon species' counts and candy counts. 

Python gets the POST data as a stream object, not a string. The Python documentation for working with streams is [here](https://docs.python.org/3/library/io.html).

- Implemented the __post__ method of the request handler class so that the user can modify class data attributes (pokemon species count and candy counts). 
- Caught errors using the built in __send_error__ method of Python's request handler class. 
- The species page, after a POST update, now displays its status as 'Updated'.  


### 8. [Wrote a template engine, added templates and a template method to the website code](https://github.com/ElAwbery/Lucky_Egg/blob/master/08.%20Add%20template%20to%20site.py)

The [wiki.Python page](https://wiki.python.org/moin/Templating) has information about template writing in Python. A general resource for understanding templating is [here](https://allwebcodesign.com/website-templates.htm). 

In this step I implemented a simple templating system in order to understand how one works:
 - Wrote templates and added them to the HTML constructor in each stage class. Used data attribute names for variables.
 - Defined the __template_substitute__ method for the pokemon parent class. This method takes an HTML string which is a template.
 - It substitutes values for variables into the template and returns the template string with substitutions. Used the Python __getattr__ method to get the required value for the variable.
 - Added code to cover for the event that the template string starts with a variable. 
 - The __html_body__ method in each stage class now returns a template string complete with substitutions. It calls the __template_substitute__ method to get the finshed string.
 

### 9. [CSS implementation](https://github.com/ElAwbery/Lucky_Egg/blob/master/09.%20Add%20CSS.py)
    
The point of this exercise was to write some CSS and understand how to add it into the application code. I wanted the server __GET__ method to send page CSS on request. The HTML for each page should include a CSS page reference in its meta data which will generate a new GET request for the CSS.

 - Added a CSS page link to the header meta for HTML pages.
 - Updated the server GET method so that it sends the CSS page on request.
 - Made some styling decisions and implemented them as part of the CSS page. 
 - I made the status line a class attribute, added it as a variable to the HTML template and applied CSS to make a colorful 'updated' banner.

## Phase 2: implementing an object relational map and MVC architecture
### 10. [Set up a database](https://github.com/ElAwbery/Lucky_Egg/blob/master/10.ii%20Load%20and%20save.py)
In Phase 1 I accessed web page data via a dictionary that mapped page names to class objects. Eventually the web app will access a data collection of several hundred pokemon objects. This step separated data storage from my application code so that I could update the code in future without interfering with the collection and storage of data.  

 - Using PHPMyAdmin in MAMP I created a MySQL table. Made a [SQL dump](https://github.com/ElAwbery/Lucky_Egg/blob/master/10.i%20SQL%20dump.sql) for the table for future reference.
 - At this stage there was one table. The database name was Pokemon. The columns in the table matched the pokemon class data attributes. 
 
Some tutorials I found helpful: 
 
[Python MySQL developer guide](https://dev.mysql.com/doc/connector-python/en/)\
[SQL tutorial](http://www.sqltutorial.org)
      
  - Imported the Python libraries __importlib__ and __mysql.connector__
  - Wrote a __load__ function. It constructs a pokemon species object (first, second or third stage) from a row in the database table using the pokemon name. The function returns a pokemon species object. 
  - Wrote a __save_to_database__ function. It takes a pokemon species object as argument and saves its data attributes to a table row. 
  - Removed dead code, including the pokemon dictionary. 

    
### 11. [Refactored the code and normalized the database](https://github.com/ElAwbery/Lucky_Egg/blob/master/11.ii%20Refactoring%20code%20to%20normalize%20database.py)

This step involved no new functionality. I refactored the code, implementing an [object relational map.](https://en.wikipedia.org/wiki/Object-relational_mapping) This was an exercise in separating out database operations from the application code. In principle I wanted to build an interface with the database that had no application specific code. The application code also must not know any information specific to the database. 

The ORM_object code assumes that user defined types (classes) have identical table names in the database. This means generic code stores and loads all attribute values:
 - Wrote an __ORM_object__ class to handle database operations. The __init__ method instantiates objects, assigning table column headings to data attribute names. This is an abstract process that will not change if new classes with unique data attributes are added to the application code.
 - Data attribute values stored in table rows are loaded using each object's unique ID.
 - After I normalized the database (see below) I realized that cross references between database tables using foreign keys could lead to multiple loads of one object. To avoid this I added an __ID_to_object__ class dictionary that guarantees an object is loaded only once per interpreter session.
 
In order to avoid repetition in the database I refactored the application class structure into two cross-referencing __ORM_obejct__ subclasses, __pokemon_family__ and __pokemon_species__.

 - The __pokemon_family__ class keeps track of candy counts and family members which are __pokemon_species__ objects. 
 - The __pokemon_species__ class keeps track of individual pokemon counts. Because the family class now tracks the species' stages, the __pokemon_species__ class no longer requires separate stage subclasses.  
 - Added HTML template variables to a __get_html__ method in the __pokemon_species__ class. 
 - Removed the subclasses that no longer contained methods or attributes of their own. 
 - Added a new HTML template variable for baby pokemon pages. (The previous code did not include the baby stage of Pokemon evolution sequences.)
 
I normalized the database to reflect the new class structure:
 - Built two new database tables with names identical to the __pokemon_species__ and __pokemon_family__ classes. (The __ORM_object__ code uses its subclass names to access database tables.) 
 - Made column names in the tables identical to the required data attributes of the two __ORM_object__ subclasses.
 - Adapted the __load__ and __store__ methods for class objects (previously part of the application code) for the __ORM_object__ class. The store method updates table data with attribute values using the object's UID to find the relevant table row.
 
I needed a way for the ORM_object code to interface with the application code (the pokemon classes) without using any information specific to the application. To do this I used UIDs for all ORM objects. The application code does not know the UIDs of any of its objects: these are specific to the database and used only in the __ORM_object__ scope. 
 - Added UID columns to the pokemon_species and pokemon_familes tables. The family UID is distinct from the individual species UID. The UIDs are not global (a family object might end up with the same UID as a species object) so the __ID_to_object__ dictionary uses both table name and UID for its keys. 
 - Wrote a __value_to_ORM_object__ helper function. This gets the UID for an ORM_object using a data attribute then looks for the object in the dictionary. If the object is not in the dictionary, it calls the __ORM_object__ class to instantiate a new object and memoizes it.
 - Families in the pokemon_families table should know which species are family members and individual pokemon in the pokemon_species table should know which family they belong to. The family column in the pokemon_species table now contains a foreign key, the family UID. The evolution stages columns in the pokemon_family table contain foreign keys to individual species in the pokemon_species table.


### 12. [Modularization:](https://github.com/ElAwbery/Lucky_Egg/tree/master/12.%20Modularization)

After the refactoring in step 11 I could easily reorganize the program into a modular [MVC](https://en.wikipedia.org/wiki/Model–view–controller) architecture. 

The [database_ORM module](https://github.com/ElAwbery/Lucky_Egg/blob/master/12.%20Modularization/database_ORM.py) expresses the model.

I separated the server code from the application code into two modules. The [application_code module](https://github.com/ElAwbery/Lucky_Egg/blob/master/12.%20Modularization/application_code.py) constructs the web page view:
 - Updated the application code to call the server and talk to it with __pokemon_handler__, an HTTPRequestHandler subclass.
 - Wrote __get_router__ and __post_router__ methods for the __pokemon_handler__ subclass. These constitute the controller of the MVC architecture.
- Wrapped the web server in a function so that it no longer runs on loading. The server is now called by the application code. In principle the [server module](https://github.com/ElAwbery/Lucky_Egg/blob/master/12.%20Modularization/server.py) can now process any browser request and call the application's router methods.
 - Additionally I separated out the [template engine](https://github.com/ElAwbery/Lucky_Egg/blob/master/12.%20Modularization/template.py) from the application module. It contains no application specific code. 
     
 
### 13. [Prevented SQL injection attacks and added store on set](https://github.com/ElAwbery/Lucky_Egg/tree/master/13.%20Prevent%20SQL%20injection%20attacks)

 - Added prepared cursor objects into the database_ORM module and used parameters to update table values.
 - Integrated set and store functionality into the ORM code, replacing the store method of previous versions with a specialized setattr.  
 - Updated the application code accordingly so that it no longer sets attributes.

 
## Phase 3: finalizing the web app
### 14. [Replaced home built template engine with Jinja2](https://github.com/ElAwbery/Lucky_Egg/tree/master/14.%20Jinja2)

My intention in each stage of this project is to learn the functionality of a part of the web framework, then replace it with an off-the-shelf program, understanding how it fits with the whole. In this step instead of augmenting my home-built template engine with branching options, I replaced it with the more powerful Jinja2:

 - Added base template .html file with four child templates for pokemon species stages.
 - Added functionality to render templates for pokemon species.
 - Updated HTML variables in the application code.


### 15. [Added tabular view](https://github.com/ElAwbery/Lucky_Egg/tree/master/15.%20Tabular%20view)
By now the Lucky Egg app shows the user a page for each of their pokemon species, with family relationships, pokemon count and candy count. The user can browse between species page views, but can't yet see all of their pokemon on one page. 

This step builds a new page view. It shows a tabular view of all the pokemon species in the database in rows according to family stages. For example, Squirtle, Wartortle, Blastoise are all on one row and the baby column in that row is empty, because the Squirtle family does not have a baby pokemon. 

 - Updated template rendering function to include a tabular page view of all pokemon species in all families.
 - Added 'get all objects of a given class' functionality to the ORM code and separated the __UID_to_object__ method out into a helper function.
 - Added an all_pokemon CSS stylesheet to the pokemon handler class
 - Updated __get_router__ and __post_router__ request handling accordingly
 - Removed status line attribute from the pokemon class and made it a template variable instead
 
<br>
     
Thanks to [@meaningness](https://twitter.com/Meaningness) for advice on architectural design and code review. 



