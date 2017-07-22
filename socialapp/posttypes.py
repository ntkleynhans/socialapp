# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from postmanager import Post

class MessagePost(Post):
    """ A message post that has a title and message body
    """
    def __init__(self, post_date, user, resource_link):
        Post.__init__(self, post_date, user, resource_link)
        self.message_title = None
        self.message_body = None

    def create(self, form):
        """ Create a new message or open an exising message
        """
        pass

    def save(self):
        """ Save any edits
        """
        pass

    def delete(self):
        """ Delete the message
        """
        pass

    def message_title(self):
        """ Return the message title
        """
        return message_title

    def message_body(self):
        """ Return the message text body
        """
        return message_body

