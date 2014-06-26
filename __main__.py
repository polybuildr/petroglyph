#!/usr/bin/env python

from watcher import Watcher

from reader import Reader
from watcher import Watcher
from writer import Writer

watcher = Watcher()
reader = Reader()
writer = Writer()

changed_files = watcher.get_posts_meta(only_changed = True)
for post in reader.read_posts(changed_files):
    writer.write_post(post)

all_posts = reader.read_posts(watcher.get_posts_meta())

writer.update_homepage(all_posts)
watcher.update_posts_meta()
