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

# password storage
import hashlib

import psycopg2 as psql
import uuid



# TODO: Make all possible queries in this file

#
# Standard DB
#

CONNECTION_INFO = "dbname='p32004b' user='p32004b' host='reddwarf.cs.rit.edu' password='Ahx5peeyaeCh1chiingi'"

def __open_connections() -> tuple:
    """
    TODO

    Return:     conn and curr
    """
    conn = psql.connect(CONNECTION_INFO)
    curr = conn.cursor()
    return conn, curr

def __close_connections(conn: object, curr: object) -> None:
    """
    Close the connection to the database.

    conn: 	db conn object
    curr: 	db curr object
    """
    curr.close()
    conn.close()
#
# Account Creation and verification
#

def get_all_users():
    return None

def verify_credentials(username: str, password: str) -> bool:
    """
    Ensure that the given account information is valid
    by comparing the username and password to those stored in the database.
    The password is NOT retrieved from the database, rather it is
    simply used in comparison in the SQL query.

    username: String that represents a users username
    password: String that represents the users password. Handle with care

    Return: Map that has a "success" attribute which indicates whether or not the credentials are correct.
            If the credentials turn out to be incorrect the map will also have a "error" attribute that
            contains a description of why the credentials may be incorrect.
    """
    # open the db connection
    conn, curr = __open_connections()

    curr.execute('SELECT 1 FROM "user" WHERE username=%s AND password=%s', (username, __hash_password(password)))
    
    # fetch the results
    response = curr.fetchone()

    # close the db connection
    curr.close()
    conn.close()

    if response is None:
        return {"error": "Username or password is incorrect.",
                "success": False}
    else:
        return {"success": True}


def register_account(username: str, password: str, first_name: str, \
        last_name:  str, email: str, state: str, city: str, \
        street: str, street2: str, postal_code: str, interests: str) -> dict:
    """
    Register a new account to the database.
    A minimum of a username, password and interets 
    are required for registration. Everything else is optional
    (but recommended)

    username:   Username for the users account
    password:   Password for the users account
    first_name:     First name of the user
    last_name:      Last name of the user
    email:      Email address of the user
    state:      State the user lives in
    city:       City the user lives in
    street:     Street address where the user lives
    street2:    street line 2
    postal_code:    Postal code of the users area
    interests:      The users interests

    return:     Dictionary with various attributes in it. 

                If the function executed successfully the 
                following dictionary will be returned
                {'success': True, 'uuid': uuid}
                
                If the function did not execute correctly
                the following dictionary will be returned
                {'success': False, 'errors': 'explanation'}
    """
    # open the db connection
    conn, curr = __open_connections()

    # define a uuid for this user
    uu = uuid.uuid4()

    # insert into "user"
    curr.execute('INSERT INTO "user"(username, first_name, last_name, password, uuid) \
            VALUES (%s, %s, %s, %s, %s)', (username, first_name, last_name, \
                    __hash_password(password), str(uu)))


    # insert into address
    curr.execute('INSERT INTO address(street_1, street_2, city, state, postal_code, belongs_to) \
            VALUES (%s, %s, %s, %s, %s, (SELECT id FROM "user" WHERE uuid = %s))', \
                    (street, street2, city, state, postal_code, str(uu)))

    # Commit the changes to the db
    conn.commit()

    # close the db connection
    __close_connections(conn, curr)

    # return the uuid assigned to the user
    return uu
    

def is_username_taken(username: str) -> bool:
    # open the db connection
    conn, curr = __open_connections()

    curr.execute('SELECT 1 FROM "user" WHERE username=%s', (username,))

    # fetch the result
    response = curr.fetchone()

    # close the db connection
    __close_connections(conn, curr)

    # if response is None then the username has not been taken
    # if response is not None then that means someone with that username
    # already exists
    return response != None

#
# MISC
#


def __hash_password(password: str) -> str:
    """
    Hash the given password with sha256 hashing.

    password: 	The password that will be encrypted

    Return: 	Encrypted string in unicode
    """
    m = hashlib.sha256(password.encode('utf-8'))
    return m.hexdigest()


