# Social media community app

## The app

Create a Twitter/Reddit clone -- user posts a message and community can comment

## Design

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

## Views

 * Home page -- login button, register button
 * Login -- form: username(email) & password, login button, navigation bar
 * Register -- form: username(email) & password & confirm password, register button, navigation bar
 * Logout -- form: logout button
 * Main post wall (pageinated) -- form: table of posts, add message, delete message, navigation bar
 * Message detail + commments -- form: message & table of comments, navigation bar

## Thoughts

Nice to haves:

 * Add groups -- users subscribe to group. Gives a way to organise and display user-specific info
 * Different threads

