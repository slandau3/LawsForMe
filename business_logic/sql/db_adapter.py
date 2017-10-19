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
import uuid

CONNECTION_INFO = "dbname='p32004b' user='p32004b' host='reddwarf.cs.rit.edu' password='Ahx5peeyaeCh1chiingi'"


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

def verify_credentials(username: str, password: str) -> bool:
    """
    Ensure that the givne account information is valid
    by comparing the username and password to those stored in the database.
    The password is NOT retrieved from the database, rather it is
    simply used in comparison in the SQL query.

    username: String that represents a users username
    password: String that represents the users password. Handle with care

    Return: Map that has a "success" attribute which indicates whether or not the credentials are correct.
            If the credentials turn out to be incorrect the map will also have a "error" attribute that
            contains a description of why the credentials may be incorrect.
    """
    conn = psql.connect(CONNECTION_INFO)
    curr = conn.cursor()

    # curr.execute('INSERT INTO "user" values (%s, %s, %s, %s, %s, %s)', (0, "s", "stevne", "landau", "j", str(uuid.uuid1())))
    curr.execute('SELECT 1 FROM "user" WHERE username=%s AND password=%s', (username, password))
    response = curr.fetchone()

    curr.close()
    conn.close()

    if response == None:
        return {"error": "Username or password is incorrect.",
                "success": False}
    else:
        return {"success": True}


