"""
This file defines the method for connecting to the database.

Requirements:
- A system environment var that contains the connection link to MongoDB

Author:
Nicholas Prussen
"""

#Imports
from pymongo import MongoClient
import os
import sys


def get_env_var():
    """ Returns the environment variable with the connection link """
    return os.environ.get('MONGO_CONNECTION_LINK')

def create_db():
    """ Uses the connection link to create a connection obj to MongoDB 
    
        NOTE: Deployment requires a hardcoded connection link inside this file to function.
        Otherwise it will default to the set environment variable.
    """

    ###
    #
    # THIS IS WHERE YOU WILL PASTE THE HARDCODED
    # MONGO CONNECTION STRING WHEN NEEDED.
    #
    # SETTING THIS TO ANYTHING EXCEPT 'None' WILL FORCE
    # THIS PROGRAM TO USE THE HARDCODED LINK
    #
    # DO NOT PUSH A HARDCODED LINK TO GITHUB
    #
    # 'connection_link = None' - This is the default variable with no hardcoded link
    #
    ###
    connection_string = None


    #This will grab the environment variable if the link has not been set
    if connection_string is None:
        connection_string = get_env_var()

    #Check to make sure connection link was found. Exit program if not
    if(connection_string is None):
        sys.exit("Connection String was not found in ENV Var or Hardcoded")
    
    #Initiate connection with link
    client = MongoClient(connection_string)
    db = client.perf_test.test_results

    return db

#Call defs
db = create_db()