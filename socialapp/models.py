# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.

@python_2_unicode_compatible
class Post(models.Model):
    """ Basic 'Post' class
            post date - when the post was created
            user - the user who created the post
            resource_link - file name to JSON data object
    """
    post_date = models.DateTimeField('published date')
    user = models.ForeignKey(User)
    resource_link = model.CharField()

    def __str__(self):
        return "{} -- {} {} -- {}".format(self.user.first_name,
            self.user.last_name, self.post_date.strftime("%A, %d %B %Y"))

