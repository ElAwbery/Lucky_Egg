# Lucky_Egg
A full stack web development project

Incrementally builds a website starting at the lowest level of back end web development and working up from there. 

Each of the tasks below correspond to the file with the same number. 

1. Established a connection with the browser 

2. Made a web server 

3. Created a simple website
    - Modified the server code to make a three page website
    - Each of the three pages contains different text; each page has its own url 
    - Each page contains links to the other two pages
    -up Added 404 error response to the handler
  
4. Separated pages from the server (created page objects)

5. Wrote an HTML form

6. Added web forms to the page class

7. Added a POST method
    - Implemented the post method of the request handler class 
    - Client can now modify page class data attributes 
  
8. Wrote a template engine, added templates and template method to site 
    - Added templates to the HTML constructor in each stage class
    - Defined a template substitution method for the pokemon parent class 
    - Cleaned up the HTML 
  
9. Add CSS
    - Added header meta for CSS to HTML pages
    - Added code to server GET method to send CSS on request
    - Wrote simple CSS just to demonstrate that it works
    - Added status_line to HTML for "Updated", as a thing to apply CSS to
    (required minor restructuring of the HTML generation code)
    
10. Write load and save methods
     - Using MAMP with PHPMyAdmin set up a MySQL table
     - The SQL dump to make a MySQL table for the Python code to talk to is included here
     - Write Python methods to construct a Pokemon object from a row and save new data to the database using SQL strings

Thanks to [@meaningness](https://twitter.com/Meaningness) for advice on architectural design and code review. 



