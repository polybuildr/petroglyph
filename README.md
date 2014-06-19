Petroglyph
==========

Petroglyph is a a static blog generator written in Python. (Tested on 2.7.6). A sample setup can be found at the [Petroglyph sample repository](https://github.com/polybuildr/petroglyph-sample).

Put your posts in the `/posts` directory with a `.md` extension. Each post's title will be used as the post's slug when the blog is generated. Markdown support is provided using [Python Markdown2](https://github.com/trentm/python-markdown2). Include post metadata by writing posts as follows:

    ---
    title: The Post's Title
    tags: some-tag, another-tag
    extras: code
    ---
    Lorem ipsum.

To generate the blog, go to the directory which contains Petroglyph and run it using `python petroglyph`.

##Manual Setup
To set up petroglyph yourself, use the following directory structure (or modify config.py):

    /blog-directory
    |-- blog
    |-- css
    |   |   |-- main.css
    |   |   |-- normalize.css
    |   |   `-- prism.css
    |   |-- js
    |   |   `-- prism.js
    |-- includables
    |   |-- home.html
    |   |-- post.html
    |   `-- post-peek.html
    |-- petroglyph
    `-- posts
