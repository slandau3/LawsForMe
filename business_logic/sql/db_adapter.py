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
import uuid

import psycopg2 as psql




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

def verify_credentials(username: str, password: str) -> dict:
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

    curr.execute('SELECT id FROM "user" WHERE username=%s AND password=%s', (username, __hash_password(password)))
    
    # fetch the results
    response = curr.fetchone()

    # close the db connection
    curr.close()
    conn.close()


    if response is None:
        return {"username": "Username or password is incorrect.",
                "success": False}
    else:
        return {"success": True,
                "uuid": uuid.UUID(response[0])}


def register_account(username: str, password: str, first_name: str, \
        last_name:  str, email: str, state: str, city: str, \
        street: str, street2: str, interests: list) -> dict:
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
    user = uuid.uuid4()

    # insert into "user"
    curr.execute('INSERT INTO "user"(id, username, first_name, last_name, password) \
            VALUES (%s, %s, %s, %s, %s)', (str(user), username, first_name, last_name, \
                    __hash_password(password)))


    # insert into address
    curr.execute('INSERT INTO address(street_1, street_2, city, state, belongs_to) \
            VALUES (%s, %s, %s, %s, %s)', \
                    (street, street2, city, state, str(user)))

    # insert into interests
    for interest in interests:
        curr.execute("INSERT INTO interests(interest)"
                     " SELECT %s"
                     " WHERE NOT EXISTS (SELECT interest FROM interests WHERE interest = %s)",
                     (interest, interest))
        curr.execute('INSERT INTO users_and_interests("user", interest) VALUES (%s, %s)',
                     (str(user), interest))


    # Commit the changes to the db
    conn.commit()

    # close the db connection
    __close_connections(conn, curr)

    # return the uuid assigned to the user
    # TODO: figure out whether this worked or not
    return {"success": True, "uuid" : user}


def is_username_taken(username: str) -> bool:
    """
    Determine if the given username is already registered
    in the database.

    :return: True if the username is registered, False otherwise
    """
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


def update_interests(interests: list) -> None:
    """
    Link interests to the laws that affect it. It's possible
    some interests have no laws that affect them.
    """
    # open the db connection
    conn, curr = __open_connections()

    for interest in interests:
        # find federal laws that contain this interest
        curr.execute("SELECT id FROM federal_law WHERE content LIKE '%%"
                     + interest + "%%'")  # Really bad I know.

        # load the interests_and_laws table if this particular combination
        # of interest and law does not exist
        for law in curr.fetchall():
            curr.execute("INSERT INTO interests_and_laws(interest, law) "
                         "SELECT %s, %s"
                         " WHERE NOT EXISTS "
                         "(SELECT id FROM interests_and_laws "
                         "WHERE interest = %s and law = %s)",
                         (interest, law[0], interest, law[0]))

    # commit all this to the db
    # is it ok to do this here and not sooner?
    conn.commit()

    # close the connections
    __close_connections(conn, curr)


def get_laws_of_interests(user: uuid) -> dict:
    """
    TODO: docstrings
    """
    # open the db connection
    conn, curr = __open_connections()

    # Don't try to understand this query. Just know that it gets interests
    # and their corresponding laws from the db
    curr.execute("select interest, title"
                 " from (select laws.interest, laws.law"
                 ' from (select interest from users_and_interests where "user" = %s) as interests'
                 " JOIN interests_and_laws as laws"
                 " on interests.interest = laws.interest)"
                 " as t join federal_law as f on t.law = f.id",
                 (str(user),))


    response = curr.fetchall()


    conn.commit()

    __close_connections(conn, curr)

    interests_and_laws = {}
    for interest, law in response:
        interest = interest.strip()
        if interest in interests_and_laws:
            interests_and_laws[interest].add(law)
        else:
            interests_and_laws[interest] = {law}

    return interests_and_laws




def get_discussions():
    # returns all the discussions for display
    conn, curr = __open_connections()

    curr.execute('SELECT * FROM discussion')

    # don't remember if this is what it is
    response = curr.fetchall()

    __close_connections(conn, curr)

    return response

def get_threads(id):
    #returns all the threads for display
    conn, curr = __open_connections()

    curr.execute('SELECT * FROM thread WHERE thread.discussion_id = %s', (id,))

    # don't remember if this is what it is
    response = curr.fetchall()

    __close_connections(conn, curr)

    return response


def get_num_4_disc():
    # Returns number of threads per discussion, with the discussions
    conn, curr = __open_connections()

    curr.execute('SELECT rsQuery1.num, rsQuery2.* '
                 'FROM (SELECT discussion_id, COUNT(*) AS num FROM thread GROUP BY discussion_id ) AS rsQuery1'
                 ' FULL OUTER JOIN '
                 ' discussion AS rsQuery2 '
                 'ON rsQuery1.discussion_id = rsQuery2.id')

    # don't remember if this is what it is
    response = curr.fetchall()

    __close_connections(conn, curr)

    return response


def get_num_4_disc_sort(type):
    # sorted discussions according to specifier 'type' for discussion with 'id'
    conn, curr = __open_connections()
    query = 'SELECT * FROM ( SELECT rsQuery1.num, rsQuery2.* ' \
            'FROM (SELECT discussion_id, COUNT(*) AS num FROM thread GROUP BY discussion_id ) AS rsQuery1 ' \
            'FULL OUTER JOIN' \
            ' discussion AS rsQuery2 ON rsQuery1.discussion_id = rsQuery2.id ) AS foo ORDER BY {}'.format(type)
    curr.execute(query)

    response = curr.fetchall()

    __close_connections(conn, curr)

    return response



def get_num_comments(id):
    # Returns threads based on topic
    conn, curr = __open_connections()

    curr.execute('SELECT rsQuery1.num, rsQuery2.* '
                 'FROM (SELECT thread_id, COUNT(*) AS num FROM forum_comment GROUP BY thread_id ) AS rsQuery1'
                 '  RIGHT JOIN '
                 ' ( SELECT * FROM thread WHERE thread.discussion_id = %s) AS rsQuery2 '
                 'ON rsQuery1.thread_id = rsQuery2.id', (id,))

    # don't remember if this is what it is
    response = curr.fetchall()

    __close_connections(conn, curr)

    return response


def get_num_4_thread_sort(id, type):
    # sorted comments according to specifier 'type' for thread with 'id'

    conn, curr = __open_connections()
    query = 'SELECT rsQuery1.num, rsQuery2.* ' \
            'FROM (SELECT thread_id, COUNT(*) AS num FROM forum_comment GROUP BY thread_id ) AS rsQuery1' \
            ' RIGHT JOIN ( SELECT * FROM thread WHERE thread.discussion_id = {0}) AS rsQuery2 ' \
            ' ON rsQuery1.thread_id = rsQuery2.id ORDER BY {1}'.format(id, type)

    curr.execute(query)

    response = curr.fetchall()

    __close_connections(conn, curr)

    return response




def add_comments(c, thread_id, user_id: uuid):
    #adds comment to the SQL database
    conn, curr = __open_connections()
    curr.execute('INSERT INTO forum_comment(id, author, content, thread_id) \
                VALUES ((SELECT MAX(id) FROM forum_comment) + 1, '
                 '%s, %s, %s)', \
                 (str(user_id), c, thread_id))

    # don't remember if this is what it is

    conn.commit()

    __close_connections(conn, curr)

    return 0




def get_comments(idd):
    # gets comment from the SQL database for display
    conn, curr = __open_connections()

    curr.execute('SELECT * '
                 'FROM (SELECT * FROM "user") AS rsQuery1'
                 '  JOIN '
                 ' ( SELECT * FROM forum_comment WHERE forum_comment.thread_id = %s) AS rsQuery2 '
                 ' ON rsQuery1.id = rsQuery2.author', (idd,))


#    curr.execute('SELECT * FROM forum_comment WHERE forum_comment.thread_id = %s', (id,))

    response = curr.fetchall()

    __close_connections(conn, curr)

    return response


def get_words(word):
    # gets the paragraphs of words/laws from the SQL database for display
    conn, curr = __open_connections()

    curr.execute('SELECT content FROM federal_law WHERE title LIKE %s', (word,));

    #    curr.execute('SELECT * FROM forum_comment WHERE forum_comment.thread_id = %s', (id,))

    response = curr.fetchall()

    __close_connections(conn, curr)

    return response


def get_interests(user_id):
    # gets the interests of specific users from the SQL database for display

    conn, curr = __open_connections()

    curr.execute('SELECT interest FROM users_and_interests WHERE "user" = %s', (str(user_id),));

    #    curr.execute('SELECT * FROM forum_comment WHERE forum_comment.thread_id = %s', (id,))

    response = curr.fetchall()

    __close_connections(conn, curr)

    return response

get_interests('1bc72b60-1c17-4db7-b61f-f0c45b1d7bfe')



def add_interest(int, user_id):
    #adds an interest to the specified users interest list
    conn, curr = __open_connections()

    curr.execute('INSERT INTO users_and_interests("user", interest) VALUES (%s,%s)', (str(user_id), int))

    # don't remember if this is what it is
    conn.commit()
    __close_connections(conn, curr)

    return 0


def del_interest(delInt, user_id):
    # deletes an interest to the specified users interest list
    conn, curr = __open_connections()

    curr.execute('DELETE FROM users_and_interests'
                 ' WHERE "user" = %s AND interest LIKE %s', (str(user_id), delInt))

    # don't remember if this is what it is
    conn.commit()
    __close_connections(conn, curr)

    return 0



#
# MISC
#



def get_thread(id):
    conn, curr = __open_connections()

    curr.execute('SELECT * FROM thread WHERE thread.id = %s', (id,))

    # don't remember if this is what it is

    response = curr.fetchall()

    __close_connections(conn, curr)

    return response


def __hash_password(password: str) -> str:
    """
    Hash the given password with sha256 hashing.

    password: 	The password that will be encrypted

    Return: 	Encrypted string in unicode
    """
    m = hashlib.sha256(password.encode('utf-8'))
    return m.hexdigest()


def __test_grab_all_discussions():
    conn, curr = __open_connections()
    conn1, curr1 = __open_connections()

    curr.execute('select * FROM discussion')


    for record in curr:
        print(record[1])
        discussion_id = record[0]
        curr1.execute('select * '
                      'FROM thread WHERE thread.discussion_id = %s', (discussion_id,))
        for rec in curr1:
            print(rec)


    __close_connections(conn, curr)
    __close_connections(conn1, curr1)







def __test_grab_all_laws():
    conn, curr = __open_connections()

    curr.execute('select * FROM federal_law')

    for record in curr:
        print(record)

    __close_connections(conn, curr)


def __test_create_account():

    # conn, curr = __open_connections()
    # # clean up the database

    # curr.execute('delete from address where street_1=%s', ('none',)) # ok just for the sake of hte demo
    # curr.execute('delete from "user" where username=%s', ('slandau',))

    # conn.commit()
    # __close_connections(conn, curr)
    register_account("slandau", "s", "steven", "landau", "none", "none", "none", "none", "none", "none")
    
    print("account exists?", is_username_taken("slandau"))

    conn, curr = __open_connections()

    # clean up the database

    curr.execute('delete from address where street_1=%s', ('none',)) # ok just for the sake of hte demo
    curr.execute('delete from "user" where username=%s', ('slandau',))

    conn.commit()

    __close_connections(conn, curr)

def __test_grab_all_kinds():
    conn, curr = __open_connections()
    curr.execute('SELECT discussion_id, COUNT(*) FROM thread GROUP BY discussion_id')
    for record in curr:
        print(record)

    __close_connections(conn, curr)


# uncomment the line below to run the test that prints out all laws currently in the database
# __test_grab_all_laws()

# uncomment the line below to run the test that registers a user in the database, checks to see if they were registered successfully, then deletes them from the database
# __test_create_account()

# uncomment the line below to run the test that prints out all discussions with corresponding threads
#__test_grab_all_discussions()

#get_num_4_disc_sort("created_at ASC ")


get_words("Partial-Birth Abortion Ban Act");


