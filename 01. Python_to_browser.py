#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 16:21:40 2018
@author: ElAwbery

Python talks directly to the browser. 
"""

# create an html file using Python

# we used tripple quotes in case the html content includes quotes itself. 
# Everything inside the tripple quotes including single quotes, is read as part of the string. 

first_page = open('first_page.html', 'w')
        
html_page = """<html>
<head></head>
<body>
<p>This is text written in html passed as a string to a Python program.
The program stores the html string as a file on my computer.</p>
</body>
</html>"""

first_page.write(html_page)
first_page.close()


# display an html page in a browser, given the file and the location on my Mac

import os
path_string = 'file://' + os.path.abspath('Charlie/first_page.html')
print('path_string=', path_string)

import webbrowser

file_path = 'file:///Users/Charlie/Documents/All%20my%20stuff/Learning%20/STEM/Computer%20Science/WebDev/Project%201%20understanding%20basics/first_page.html'
webbrowser.open_new_tab(file_path)


# ask the user for html content to turn into a file

def make_file():
    """
    creates an html file
    """
    get_content = input("Paste the content for your html file, include your doctype, html tags and header, body etc.\n")
    get_name = input("what do you want to call your file?\n")
    
    new_html_file = open(str(get_name) + '.html', 'w')
    page_content = "" + str(get_content) + ""
    
    new_html_file.write(page_content)
    new_html_file.close()
    
        
# ask the user for a string to insert into an html boilerplate
    
def provide_html_template():
    """
    Turns content from a user into an html file
    """
    get_content = str(input("Paste the content you want to see displayed in the browser here. \n"))
    get_name = input("I am going to create an html file with your content. What do you want to call your file? \n")
    
    new_html_file = open(str(get_name) + '.html', 'w')
    
    page_content = '<html><head></head><body><p>' + get_content + '</p></body></html>'
    
    new_html_file.write(page_content)
    new_html_file.close()
    
