Petroglyph
==========

Petroglyph is a a static blog generator written in Python. (Tested on 2.7.6).

Put your posts in the `/posts` directory with a `.md` extension. Each post's title will be used as the post's slug when the blog is generated. Markdown support is provided using [Python Markdown2](https://github.com/trentm/python-markdown2). Include post metadata by writing posts as follows:

    ---
    title: The Post's Title
    tags: some-tag, another-tag
    extras: code
    ---
    Lorem ipsum.

##How to use
Go to the Petroglyph directory, and
1. Create directory called `blog`
2. Copy `js` and `css` directories from includable
3. Run `python petroglyph` to generate the blog
