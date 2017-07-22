# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from postmanager import Post
from resources import Resource
from django import forms

class MessageForm(forms.Form):
    """ Message Post form
    """
    message_title = forms.CharField()
    message_body = forms.CharField()

class MessagePost(Post):
    """ A message post that has a title and message body
    """
    def __init__(self, post_date, user, resource_link):
        Post.__init__(self, post_date, user, resource_link)
        self.message_title = None
        self.message_body = None
        self.resource = None

    def validate(self, request):
        """ Validate the message form -- need title and message
        """        
        form = MessageForm(request.POST)
        return form

    def create(self, form):
        """ Create a new message or open an exising message
        """
        self.resource = Resource(self.resource_link)
        if form is None:
            self.resource.load()
            content = self.resource.content()
            self.message_title = content["message_title"]
            self.message_body = content["message_body"]
        else:
            self.save(form.cleaned_data["message_title"], form.cleaned_data["message_body"])

    def save(self, title, body):
        """ Save any edits
        """
        self.resource.save({"message_title" : title, "message_body" : body})
        self.message_title = title
        self.message_body = body

    def delete(self):
        """ Delete the message
        """
        self.resource.delete()
        self.message_title = None
        self.message_body = None
        self.resource = None

    def message_title(self):
        """ Return the message title
        """
        return self.message_title

    def message_body(self):
        """ Return the message text body
        """
        return self.message_body

