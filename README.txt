LawsForMe is organized in a very simple and advanced way.

The main file, app.py should be run to start the webserver. All other python files can be found inside of the business_logic folder.

The business_logic folder contains folders such as "account" and "sql". 

The account folder houses files that have to do with verifying a users credentialls and generally just messing with their account information.

The sql folder contains files that have to do with sql. The sql_adapter.py file contains methods that interact with the database itself. All queries (except for those used to create the database) can be found inside this file. The db_creation.py file houses the database spec. Only attempt to source the db_creation file if you wish to create a local versiion of the database.

In order to start the program you will need to install the dependencies. Simply run the program and look at what errors it gives, when it tells you "x" module cannot be found simply do pip3 install x. You may also be able to do pip3 install setup.py however this is not guarenteed to install all of the dependencies. 

The doc directory has all files having to do with the phase submission papers and diagrams and stuff like that.

The crawler directory contains the crawler used to parse wikipedia, please disregard it.

The templates folder contains html templates that are used for the web application.

The static folder contains css files, javascript files and images.


Remember: To run the program simply do, python3 app.py



Notes:

Flask is the framework that has been used

WHEN CREATING AN ACCOUNT:
    - interests should be comma seperated
    - The algorithm to determine what laws affect what interests is fairly basic at the moment so there may be many keywords that don't give any interests. Some examples of interests that will definitely yield results are: internet, fishing
    - If you do not enter a firstname or lastname, the word "none" will be displayed in a forum comment, should you make one
    - Only username, password and interests are required to create an account!

In the forums section you can sort discussions in various ways


