#!/usr/bin/env python

from config import config, blog_config
from post import Post
import os
import re
import codecs

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))


class Writer(object):
    def __init__(self):
        pass

    def write_post(self, post):
        template = open(os.path.join(config['includables_path'], 'post.html'), 'r').read()
        
        post_dir = os.path.join(config['blog_path'], post.slug)
        head_extras = ''
        body_extras = ''
        if 'code' in post.extras:
            head_extras += '<link href="../css/prism.css" rel="stylesheet">'
            body_extras += '<script src="../js/prism.js"></script>'
        
        if not os.path.exists(post_dir):
            os.makedirs(post_dir)
        
        f = open(os.path.join(post_dir, 'index.html'), 'w')
        
        f.write(template.format(blog_title = blog_config['title'],
                              post_title = post.title,
                              post_tags = ''.join(['<span href="#" class="tag">#' + tag + '</span>' for tag in post.tags]),
                              post_content = post.content,
                              post_date = custom_strftime('{S} %B, %Y', post.date),
                              head_extras = head_extras,
                              body_extras = body_extras,
                              post_url = ''.join([blog_config['url'], post.slug, '/']),
                              blog_url = blog_config['url'],
                              post_slug = post.slug,
                              blog_shortname = blog_config['shortname'] if 'shortname' in blog_config else blog_config['title'].replace(' ','').lower()))
        
    def write_posts(self, posts):
        for post in posts:
            self.write_post()
    
    def update_homepage(self, posts):
        template = open(os.path.join(config['includables_path'], 'home.html'), 'r').read()
        peek_template = open(os.path.join(config['includables_path'], 'post-peek.html'), 'r').read()
        peeks = []
        for post in posts:
            more_matches = re.findall('.*<!--more-->', post.content, re.MULTILINE | re.DOTALL)
            more_match = more_matches[0] if len(more_matches) > 0 else ''
            preview = True
            if not more_match.strip():
                more_match = post.content
                preview = False
            peeks.append(peek_template.format(post_title = post.title,
                            post_tags = ''.join(['<span href="#" class="tag">#' + tag + '</span>' for tag in post.tags]),
                            post_content = post.content,
                            post_peek = more_match,
                            post_date = custom_strftime('{S} %B, %Y', post.date),
                            post_slug = post.slug,
                            permalink_text = 'Continue reading' if preview else 'Permalink'))
        peeks_html = ''.join(peeks)
        
        f = codecs.open(os.path.join(config['blog_path'], 'index.html'), "w", 
                          encoding="utf-8", 
                          errors="xmlcharrefreplace"
        )

        f.write(template.format(blog_title = blog_config['title'],
                                blog_description = blog_config['description'],
                                blog_author = blog_config['author'],
                                posts = peeks_html))
