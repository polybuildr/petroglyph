#!/usr/bin/env python

from datetime import datetime

class Post(object):
    def __init__(self, slug, title='', tags=[], content='', date=datetime.now(), extras=[]):
        self.title = title
        self.tags = tags
        self.content = content
        self.date = date
        self.slug = slug
        self.extras = extras