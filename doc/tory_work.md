# Work for Tory

## Create Account Page
Tory's current job is to create a page that specializes in account creation.

### Page specification 
The fields the create account page should have are as follows, starred fields are required


| \*Username  |
| \*Password  |
| Email       |
| State       |
| City        |
| Street      |
| Street 2    |
| Postal code |
| \*Interests |


1. Username - text input that cannot be empty and must be unique
2. Password - cannot be empty and should contain at least x characters and one special character
3. Email - can be empty but must be a valid address (does not need to actually exist just must be a valid email)
4. State - can be empty, dropdown menu where users can choose what state they live in. The default value should be ---- which indicates the user does not wish to disclose their state.
5. City - can be empty, text field where the user can enter their city if they so desire
6. Street - Can be empty, the street address at which this user lives.
7. Street 2 - Can be empty, line 2 of the users address, typically left empty.
8. Postal code - can be left empty, the zip code of the user.
9. Interests - Text field where the user inputs their interests which should be seperated by commas. It might be beneficial to show a red mark on invalid interests (interests that return no results). More on this later.

### POST Data
#### To Server
The data posted to the server is a map linking attribute names to the value the user inputted. In HTML, when you specify the fields such as "username", you need to add another attribute inside the opening tag. Ex for username: 
```html
<input type="text" name="username"> 
```
. The name for all the fields should be as follows:


| field       | name arg   |
|-------------+------------|
| Username    | username   |
| Password    | password   |
| Email       | email      |
| State       | state      |
| Street      | street     |
| Street 2    | street2    |
| Postal code | postalCode |
| Interests   | interests  |

#### From Server
The server should respond with a JSON map (which you will need to parse using javascript). The map will contain names of fields as a key and the error message that should be displayed as the related value. Ex:
```json
{
    {
    "username" : "Username cannot be left empty.",
    "password" : "Password must be greater than 8 characters and contain at least one special character."
    }
}
```

If everything the user inputted was valid then the user will be redirected to the home page (you don't need to worry about this for now).

