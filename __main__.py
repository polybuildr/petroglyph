#!/usr/bin/env python

from watcher import Watcher

from reader import Reader
from watcher import Watcher
from writer import Writer

watcher = Watcher()
reader = Reader()
writer = Writer()

changed_files = watcher.get_changed_posts()
for post in reader.read_posts(changed_files):
    writer.write_post(post)

writer.update_homepage(reader.read_posts(watcher.get_posts_list()))
watcher.update_posts_meta()
