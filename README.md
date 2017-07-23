# Social media community app

## Quickstart

Clone Social App source:

```bash
$  git clone https://github.com/ntkleynhans/socialapp.git
```

Create Python virtual environment:

```bash
$ virtualenv env
```
Use new Python virtual environment:

```bash
source env/bin/activate
```

Install Python Django:
``` bash
$ pip install django
```

Migrate site and app database entries:
```bash
$ cd socialapp/
$ ./manage.py migrate
```

Create a super user for admin access:
```bash
$ ./manage.py createsuperuser
```

For main application use a Web browser to navigate to:
```
http://127.0.0.1:8000/socialapp/
```

To access the administration inteface use a Web browser and navigate to:
```
http://127.0.0.1:8000/admin/
```

### Social media community application

The current application (in the master branch of Github) allows a user to register with system,
login as the registered user, browser community message posts, and delete posts owned by the users.
Currently, only message posts are supported. The interface provides the following views:

 * Home page -- login button, register button
 * Login -- form: username(email) & password, login button, navigation bar
 * Register -- form: username(email) & name & surname & password & confirm password, register button, navigation bar
 * Main post wall (pageinated, 5 posts per page) -- form: table of posts, add post, logout, navigation bar
 * Create post -- form: title & message text, logout, cancel, navigation bar
 * Message detail -- information group: date & owner & title & message, delete post (if owned by logged in user), logout, navigation bar

A user can logout when the Logout button is provided on a specific view.

### TODO:

* Provide a single view
* Code refactor
* Add more post types such as comments

## INITIAL IDEAS
### The app

Create a Twitter/Reddit clone -- user posts a message and community can comment

### Design

My app revolves are the idea of a generic user `Post`.

Main class -- `Post` -- with inherited classes:

 * `PostMessage(Post)` - main post that users can comment on. Will be displayed in main view and can be selected
 * `PostComment(Post)` - is asscociated with a message and is displayed in message detail view

Generate a Post using `PostFactory`.

Each `Post` has a resources associated with it -- *image*, *audio*, *text*, etc...
Will stick to text for now.

Main class -- `Resource` -- with inherited classes:

 * ResourceText(Resource) -- a text resources associated with a Post. Count be a message or comment.

(NOTE: ?? wonder if resource should inherit from Post ??)

Recursively populate messages, comments and delete comments

### Views

 * Home page -- login button, register button
 * Login -- form: username(email) & password, login button, navigation bar
 * Register -- form: username(email) & password & confirm password, register button, navigation bar
 * Logout -- form: logout button
 * Main post wall (pageinated) -- form: table of posts, add message, delete message, navigation bar
 * Message detail + commments -- form: message & table of comments, navigation bar

### Thoughts

Nice to haves:

 * Add groups -- users subscribe to group. Gives a way to organise and display user-specific info
 * Different threads

