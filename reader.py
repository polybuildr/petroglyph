#!/usr/bin/env python

import os
from config import config
import markdown2
from datetime import date
from post import Post
import re
import codecs

class Reader(object):
    def __init__(self, path = config['posts_path']):
        self.path = path
        
    def _read_post(self, post_meta):
        rel_file_path = post_meta.slug
        file_path = os.path.join(self.path, rel_file_path + config['posts_extension'])
        if (os.path.isfile(file_path)):
            html = markdown2.markdown(codecs.open(file_path, mode="r", encoding="utf-8").read(), extras=['metadata'])
            html_code = re.sub(r'<code>\|([a-z]*)\|\n', r'<code class="language-\1">', html)
            html_code = html_code.replace(r'<pre><code', r'<pre class="line-numbers"><code')
            html_code = html_code.replace("\n</code></pre>", r'</code></pre>')
            tags = []
            extras = []
            title = ''
            if 'tags' in html.metadata:
                for tag in html.metadata['tags'].split(','):
                    tags.append(tag.strip())
            if 'title' in html.metadata:
                title = html.metadata['title']
            if 'extras' in html.metadata:
                for extra in html.metadata['extras'].split(','):
                    extras.append(extra.strip())
            mtime = post_meta.mtime
            return Post(rel_file_path, title, tags, html_code, mtime, extras)
            
    def read_posts(self, posts_meta):
        return [self._read_post(f) for f in posts_meta]
