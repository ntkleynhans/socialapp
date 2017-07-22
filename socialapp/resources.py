# -*- coding: utf-8 -*-

import uuid
import base64
import os
import json
import codecs

DATA_DIR = "socialapp/storage"

def generate_resource():
    """ Generate a unique filename for the resource link
    """
    return os.path.join(DATA_DIR, base64.b64encode(str(uuid.uuid4())))


class Resource(object):
    """ Handle file system resources
        Each Post has an associated resource
    """
    def __init__(self, name):
        self.fname = name
        self.data = None

    def load(self):
        """ Load the data from resource -- return dict
        """
        with codecs.open(self.fname, "r", "utf-8") as f:
            self.data = json.load(f)

    def save(self, payload):
        """ Save the payload -- payload should be dict
        """
        with codecs.open(self.fname, "w", "utf-8") as f:
            json.dump(payload, f)
        self.data = payload

    def delete(self):
        """ Remove resource
        """
        os.remove(self.fname)
        self.fname = None
        self.data = None

    def content(self):
        """ Return the resource content
        """
        return self.data

    def name(self):
        """ Return the resource name
        """
        return self.fname


