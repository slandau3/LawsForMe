# Work for Talha

## Login

Your job is to create the login page. 

### Design specification

| Attribute        | Attribute Name  |
|------------------|-----------------|
| Username         | username        |
| Password         | password        |

The Attribute column indicates how the attribute will be referenced in the documentation .The Attribute Name is what the html attribute's name should be. Ex:
```html
<input type="text" name="username">
<input type="text" name="password">
```

There should also be a link to account recovery (to be implemented) and a link to account creation (if the user needs to create an account). Of course there must also be a submit button.

Upon submission of the form. The form should post to "/login/".

### Communicating with server
When the user submits the information to the server the server will either return data in JSON format indicating what the error was or the user will be redirected (which you don't have to worry about). You may display the error message in any way you see fit. 

An example of the data returned by the server:

```JSON
{
    "error" : "Incorrect username or password."
}
```
