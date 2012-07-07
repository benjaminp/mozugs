import hashlib
import os
import random
import time

from sqlalchemy import types

def get_script_name(environ):
    """Returns the equivalent of the HTTP request's SCRIPT_NAME environment
    variable. If Apache mod_rewrite has been used, returns what would have been
    the script name prior to any rewriting.
    """
    # If Apache's mod_rewrite had a whack at the URL, Apache set either
    # SCRIPT_URL or REDIRECT_URL to the full resource URL before applying any
    # rewrites.
    script_url = environ.get('SCRIPT_URL', '')
    if not script_url:
        script_url = environ.get('REDIRECT_URL', '')
    if script_url:
        name = script_url[:-len(environ.get('PATH_INFO', ''))]
        if not name.endswith("/"):
            name += "/"
        return name
    return "/"


def make_key(salt):
    """Try to create a good key for sessions. Ripped from Django."""
    raw = "%s%s%s%s" % (random.randrange(0, 2 << 63), os.getpid(), time.time(), salt)
    return hashlib.md5(raw).hexdigest()


# like for choice fields - like severity -- from http://stackoverflow.com/a/6264027
class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        print(self.choices)
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]
