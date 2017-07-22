# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import importlib

class Post(object):
    """ Basic Post
    """
    def __init__(self, post_date, user, resource_link):
        self.post_date = post_date
        self.user = user
        self.resource_link = resource_link

    def create(self):
        raise NotImplementedError("Create method missing")

    def save(self):
        raise NotImplementedError("Save method missing")

    def delete(self):
        raise NotImplementedError("Delete method missing")

class PostManager(object):
    def __init__(self, post_date, user, resource_link, name):
        self.post_date = post_date
        self.user = user
        self.resource_link = resource_link
        self.NewPost = self.choose_post(name)

    def choose_post(self, name):
        """ Choose a post type based on the name from posttypes module
        """
        try:
            module = importlib.import_module("posttypes")
            method = getattr(module, name)
            return method(self.post_date, self.user, self.resource_link)
        else Exception as E:
            raise NotImplementedError(str(E))

    def create(self, form):
        """ Create the requested post
        """
        # TODO: Not sure this is actually how it is done for factories!!
        self.NewPost.create(form)
        return self.NewPost

