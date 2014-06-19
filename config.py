import os

petroglyph_path = os.path.dirname(os.path.realpath(__file__))

cwd = os.getcwd()

blog_config = {
    'title'         : 'Blog Title',
    'author'        : 'Blog Author',
    'description'   : 'Blog Description'
}

config = {
    'meta_path'         : os.path.join(petroglyph_path, 'meta'),
    'posts_path'        : os.path.join(cwd, 'posts'),
    'includables_path'  : os.path.join(cwd, 'includables'),
    'blog_path'         : os.path.join(cwd, 'blog'),
    'posts_extension'   : '.md'
}