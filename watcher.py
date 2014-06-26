#!/usr/bin/env python

import os
from config import config
import hashlib
import datetime as dt
from ast import literal_eval
import csv

class Watcher(object):
    def __init__(self, path = config['meta_path']):
        self.path = path
    
    class Meta(object):
        def __init__(self, slug = '', hash = '', mtime = dt.datetime.now(), from_tuple = None):
            if not from_tuple:
                self.slug = slug
                self.mtime = mtime
                self.hash = hash
            else:
                self.slug = from_tuple[0]
                self.hash = from_tuple[1]
                self.mtime = dt.datetime(int(from_tuple[2]), int(from_tuple[3]), int(from_tuple[4]), int(from_tuple[5]), int(from_tuple[6]), int(from_tuple[7]))
        
        def repr_tuple(self):
            return (self.slug, self.hash, self.mtime.year, self.mtime.month, self.mtime.day, self.mtime.hour, self.mtime.minute, self.mtime.second)
        
        def __str__(self):
            return 'Meta object ' + str(self.repr_tuple())
        def __repr__(self):
            return self.__str__()

    def _file_hash(self, f, block_size=2**20):
        md5 = hashlib.md5()
        while True:
            data = f.read(block_size)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()
    
    def update_posts_meta(self, new_meta = None):
        posts_meta_path = os.path.join(self.path, 'posts.csv')
        if not new_meta:
            new_meta = self.generate_posts_meta()
        
        old_meta = self._read_posts_meta_file()
        new_meta = sorted(new_meta, key = lambda post: post.mtime)
        
        old_meta_slugs = [meta.slug for meta in old_meta]
        new_meta_slugs = [meta.slug for meta in new_meta]
        meta = []
        
        for meta_item in old_meta:
            if meta_item.slug in new_meta_slugs:
                new_meta_item = new_meta[new_meta_slugs.index(meta_item.slug)]
                meta_item.hash = new_meta_item.hash
                meta.append(meta_item)

        for meta_item in new_meta:
            if meta_item.slug not in old_meta_slugs:
                meta.append(meta_item)

        if not os.path.exists(self.path):
            os.mkdir(self.path)
        
        with open(posts_meta_path, 'wb') as posts_meta:
            for meta_item in meta:
                meta_writer = csv.writer(posts_meta)
                meta_writer.writerow(meta_item.repr_tuple())
    
    def _read_posts_meta_file(self):
        posts_meta_path = os.path.join(self.path, 'posts.csv')
        meta = []
        if (os.path.isfile(posts_meta_path)):
            with open(posts_meta_path, 'rb') as posts_meta:
                meta_reader = csv.reader(posts_meta)
                for row in meta_reader:
                    meta.append(self.Meta(from_tuple = tuple(row)))
        return meta
    
    def generate_posts_meta(self, write = False):
        meta = []
        for root, dirs, files in os.walk(config['posts_path']):
            for f in files:
                file_path = os.path.join(root, f)
                opened_file = open(file_path, 'rb')
                file_hash = self._file_hash(opened_file)
                file_mtime = dt.datetime.fromtimestamp(os.path.getmtime(file_path))
                slug = os.path.splitext(f)[0]
                meta.append(self.Meta(slug, file_hash, file_mtime))
        return meta
    
    def get_posts_list(self):
        posts_meta_path = os.path.join(self.path, 'posts.csv')
        new_meta = self.generate_posts_meta()
        
        old_meta = self._read_posts_meta_file()
        new_meta = sorted(new_meta, key = lambda post: post.mtime)
        
        old_meta_slugs = [meta.slug for meta in old_meta]
        new_meta_slugs = [meta.slug for meta in new_meta]
        meta = []
        
        for meta_item in old_meta:
            if meta_item.slug in new_meta_slugs:
                meta.append(meta_item)

        for meta_item in new_meta:
            if meta_item.slug not in old_meta_slugs:
                meta.append(meta_item)
                
        return meta[::-1]
    
    def get_changed_posts(self):
        posts_meta_path = os.path.join(self.path, 'posts.csv')
        new_meta = self.generate_posts_meta()
        
        old_meta = self._read_posts_meta_file()
        new_meta = sorted(new_meta, key = lambda post: post.mtime)
        
        old_meta_slugs = [meta.slug for meta in old_meta]
        new_meta_slugs = [meta.slug for meta in new_meta]
        meta = []

        for meta_item in new_meta:
            if meta_item.slug not in old_meta_slugs:
                meta.append(meta_item)
            else:
                old_meta_item = old_meta[old_meta_slugs.index(meta_item.slug)]
                if old_meta_item.hash != meta_item.hash:
                    meta_item.mtime = old_meta_item.mtime
                    meta.append(meta_item)

        return meta[::-1]
    
    def get_posts_meta(self, only_changed = False):
        posts_meta_path = os.path.join(self.path, 'posts.csv')
        new_meta = self.generate_posts_meta()
        
        old_meta = self._read_posts_meta_file()
        new_meta = sorted(new_meta, key = lambda post: post.mtime)
        
        old_meta_slugs = [meta.slug for meta in old_meta]
        new_meta_slugs = [meta.slug for meta in new_meta]
        meta = []

        for meta_item in new_meta:
            if meta_item.slug not in old_meta_slugs:
                meta.append(meta_item)
            else:
                old_meta_item = old_meta[old_meta_slugs.index(meta_item.slug)]
                if old_meta_item.hash != meta_item.hash:
                    old_meta_item.hash = meta_item.hash
                    if only_changed:
                        meta.append(old_meta_item)
                if not only_changed:
                    meta.append(old_meta_item)
        
        return sorted(meta, key = lambda post: post.mtime, reverse = True)
