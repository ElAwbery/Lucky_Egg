#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 15:17:03 2019

@author: ElAwbery
"""

# Importlib needed in order to import mysql.connector
# Spyder gives a 'not used' alarm because it doesn't know it's being used 
# behind the scenes
import importlib
import mysql.connector

PORT = 80

# Because our ORM code is generic, we assign the database variable outside of 
# the ORM_object class

database_name = 'Pokemon'

"""
We have modularized our code into an MVC architecture. The database_ORM module
allows us to express our model.   
    
The database_ORM handles all database operations. It is the interface 
between our application code and the database. We assume our user defined 
types (classes) have identical table names in the database so that all our
object attribute values can be stored to and loaded from the database with 
generic code. 

The ORM_object class instantiates objects, assigning its table column headings 
to data attribute names. This is an abstract process that will not change 
if new classes with unique data attributes are added to the application code. 
Data attribute values stored in table rows are loaded using each 
object's unique ID.
  
Circular references between database tables using foreign keys could lead to 
multiple loads of one object. To avoid this the ORM_object class keeps an 
ID_to_object dictionary that guarantees an object is loaded only once per 
interpreter session. The value_to_ORM_object helper function fetches objects
from the class dictionary and calls the ORM_object class to instantiate new objects.

The ORM_object class uses its subclass names to access database tables. 
"""

class ORM_object(object):
    """
    Loads a database object from corresponding table
    Stores its data attributes to its table
    """
    # Class variable dict maps object values to IDs
    # This prevents creating multiple objects for the same ID
    ID_to_object = {}
    
    # The init method constructs the database object 
    def __init__(self, ID):
        """
        Retrieves column headings from the database table 
        Sets object data attribute names with column headings
        Selects stored object values from table
        Sets object attribute values
        """
        # object.__setattr__ is the root class' method, which just sets. The ORM_object
        # class has its own separately defined __setattr__ method that updates the 
        # database, so application code does not have to call a store method explicitly.
        # We use object.__setattr__ during initialization (which is the 
        # database load) to avoid triggering the database update that our
        # specialized __setattr__ causes.
        
        # The class name must be identical to the table name
        object.__setattr__(self, 'table', self.__class__.__name__)
        
        # Add the object to the class dictionary (this must be done before 
        # loading the data attribute values otherwise the foreign keys will 
        # cause multiple loads
        
        # Keys are a tuple (table_name, UID), because UIDs are not global 
        # (different tables in the database may use the same UID for a row)
        ORM_object.ID_to_object[(self.table, ID)] = self
        
        # Create a connection to the mySQL server
        # These are the default login details
        # Port 8889 is the port MAMP uses to connect to MySQL
        # This recreates the connection on every load, which is inefficient but 
        # OK for now
        # use_pure disables the use of CEXT which is enabled by default but 
        # does not support prepared statements
        cnx = mysql.connector.connect(user='root', password='root',
                                      host='127.0.0.1', port="8889",
                                      database = database_name, use_pure=True)
        
        # We have no multi-statement transactions, so it's fine to use 
        # autocommit
        cnx.autocommit = True 
        # Create a MySQLCursorPrepared object
        # This cursor enables execution of prepared statements which prevent
        # vulnerability to SQL injection attacks
        cursor = cnx.cursor(prepared = True)

        # Prepared statement parameters can only be values, not tables or columns.
        # Even though the code here is not using any user-supplied data it is 
        # good practice to use a prepared statement anyway just to be sure that
        # an attack is impossible in future, & for code consistency.
        SQL_get_columns = "SELECT * from " + self.table + " LIMIT 1"
        
        # Get the column names from the table
        cursor.execute(SQL_get_columns)
        object.__setattr__(self, 'columns', cursor.column_names)
        # Clear the cursor so it's willing to read again
        cursor.fetchone()
        
        # In case of a column being a foreign key we need to substitute the
        # object for the ID:
       
        # Get a list of foreign keys for this table.
        # All our tables have a UID primary key column. A foreign key in one 
        # table is always a UID in another one
        SQL_get_foreign_keys = "SELECT COLUMN_NAME, REFERENCED_TABLE_NAME from\
                       information_schema.KEY_COLUMN_USAGE WHERE\
                       CONSTRAINT_SCHEMA = '" + database_name + "'\
                       AND TABLE_NAME = '" + self.table + "'\
                       AND REFERENCED_COLUMN_NAME = 'UID'"
        cursor.execute(SQL_get_foreign_keys)
        keys_and_tables = cursor.fetchall()
        
        # Store foreign keys as dictionary keys with their referenced tables for 
        # values
        foreign_keys = {}
        
        for pair in keys_and_tables:
            foreign_keys[pair[0]] = pair[1]
        # use parameters for prepared cursor statement where possible
        # ID is a value so it can be parameterized
        SQL_get_row = "SELECT * FROM " + self.table + " WHERE UID = %s;" 
    
        # load the row for this UID
        cursor.execute(SQL_get_row, (str(ID),))
        
        # a tuple containing the values, extracted from the 1-long row list:
        data_for_attribute_values = cursor.fetchall()[0]
        
        index = 0

        # This loop sets data attribute names for the object and assigns
        # values to them
        for column_name in self.columns:
        
            attribute_value = data_for_attribute_values[index]
                
            # First check if the value is a foreign key
            # If it is get the object with the foreign key UID
            if column_name in foreign_keys and attribute_value != None:
                referenced_table = foreign_keys[column_name]
                try:
                    foreign_object = ORM_object.ID_to_object[(referenced_table, attribute_value)]
                # If the object is not already saved to the ORM_object class 
                # dictionary:
                except KeyError:
                    # Get the class object using the table name
                    _class = get_subclass_from_name(ORM_object, referenced_table)
                    # Load a new object
                    foreign_object = _class(attribute_value)  
                # Make data attribute name from the column name and assign the 
                # value. eg: the attribute self.UID is made from column name 'UID' 
                # and assigned UID value from the table           
                finally:
                    object.__setattr__(self, column_name, foreign_object)
            
            else:
                object.__setattr__(self, column_name, attribute_value)
                
            index += 1

        # Close the cursor and connection to tidy up
        cursor.close()
        cnx.close()
    
    # __setattr__ method replaces store method. In previous versions, application
    # code set data attributes and ORM code stored them. This method integrates 
    # set and store functionality into the ORM. All updated attribute values are set 
    # here and stored to database. 
    def __setattr__(self, attr, value):
        """
        Sets attribute value.
        Automatically updates table data with data attribute values using the object's 
        UID to find the relevant table row.
        """
        object.__setattr__(self, attr, value)
        
        # not all data attributes are stored in the database
        if attr in self.columns:
            
            # Create a connection to the mysql server
            cnx = mysql.connector.connect(user='root', password='root',
                                          host='127.0.0.1', port="8889",
                                          database = database_name, use_pure = True)
            
            cursor = cnx.cursor(prepared = True)
            
            # We have no multi-statement transactions, so it's fine to autocommit
            cnx.autocommit = True
            
            # By API contract, the attr must be the same as the column name
            SQL_update_row = "UPDATE " + self.table + " SET `" + attr + "`\
                            = %s  WHERE `UID` = %s;"
            
            cursor.execute(SQL_update_row, (value, str(self.UID)))
            # Close the cursor and database to tidy up
            cursor.close()
            cnx.close()

# In previous versions, this was accomplished with globals(), but that doesn't 
# work across modules, and anyway this is cleaner. This only goes one level
# down in the subclass hierarchy, which is adequate for current purposes.
def get_subclass_from_name(_class, name):
    """
    name is a string, name of subclass
    returns the subclass
    """
    assert type(name) == str
    for subclass in _class.__subclasses__():
        if subclass.__name__ == name:
            return subclass


# The value_to_ORM_object function is the main interface between the application
# code and the ORM. The application code does not use UIDs, those are internal
# to the ORM. The application code identifies an object using a unique data 
# attribute which it supplies here. 
# This function gets the UID using the supplied data attribute name and returns 
# the object for that UID. 
# Subclass data attributes must match database table column names exactly
        
def value_to_ORM_object(class_name, attribute_name, value):
    """
    class_name, attribute_name and value are all strings
    Attribute name is equal to column name in table
    Selects UID from the table row where the value matches the given column
    name
    Retrieves ORM_object from class dictionary using UID or calls ORM_object 
    class to instantiate a new object
    """
    assert type(class_name)==str and type(attribute_name)==str and type(value)==str
    
    cnx = mysql.connector.connect(user='root', password='root',
                                  host='127.0.0.1', port="8889",
                                  database = database_name, use_pure = True)
    
    cursor = cnx.cursor(prepared = True)
    
    SQL_get_UID = "SELECT UID FROM " + class_name + " WHERE `" + attribute_name + "` = %s;" 
                   
    cursor.execute(SQL_get_UID, (value,))
    UID = cursor.fetchone()[0]
    
    if (class_name, UID) not in ORM_object.ID_to_object:
        _class = get_subclass_from_name(ORM_object, class_name)
        new_object = _class(UID)
        ORM_object.ID_to_object[(class_name, UID)] = new_object
        
    cursor.close()
    cnx.close()
        
    return ORM_object.ID_to_object[(class_name, UID)]
