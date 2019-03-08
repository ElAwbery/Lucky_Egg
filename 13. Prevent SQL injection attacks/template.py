#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 16:47:32 2019

@author: Charlie
"""

def substitute(_object, template):
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
            new_value = attribute_value_for_template(_object, 
                                                    template_segments[index])
            
            if isinstance(new_value, int):
                new_value = str(new_value)
                
            if not isinstance(new_value, str):
                raise TypeError

            html += new_value
                
        index += 1

    return html
    
# Helper function for template_substitute method
def attribute_value_for_template(_instance, index):
    """
    index is a string of attributes separated by dots
    """
    attributes = index.split('.')
    next_instance = getattr(_instance, attributes[0])
    
    # Temporary kludge: we actually need branches in our template engine
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
    