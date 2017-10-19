"""
File: db_adapter.py
Description: The functions in this file provide an interface between 
             the rest of the program and the databaes. This file should
             contain every function that is needed to interact with the
             database. The functions in this file do not do any 
             verification aside from constraint checks when 
             performing queries.

Authors: Steven Landau, Tory Leo, Talha Azhar
"""

import psycopg2 as psql


# conn = psycopg2.connect("dbname='p32004b' user='p32004b' host='reddwarf.cs.rit.edu' password='Ahx5peeyaeCh1chiingi'")
# curr = conn.cursor()

# TODO: Make all possible queries in this file

#
# SELECTS
#
def get_all_users():
    return None


#
# INSERTS
#


#
# MISC
#

def verify_password(username: str, password: str) -> bool:
    """
    Ensure that the givne account information is valid
    by comparing the username and password to those stored in the database.
    The password is NOT retrieved from the database, rather it is
    simply used in comparison in the SQL query.

    username: String that represents a users username
    password: String that represents the users password. Handle with care

    Return: boolean indicating whether or not the credentials are valid
    """
    pass

