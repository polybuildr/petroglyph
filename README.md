Petroglyph
==========
[![Build Status](https://travis-ci.org/polybuildr/petroglyph.svg?branch=master)](https://travis-ci.org/polybuildr/petroglyph)

Petroglyph is a Python-based static blog generator. (Tested on 2.7.6).

## Installation

Petroglyph is now a pip package! You can install petroglyph by simply doing:
```bash
$ sudo pip install petroglyph
```

If you don't have `pip`, first install pip using your package manager.

```bash
$ sudo apt-get install python-pip #Ubuntu, etc.
$ sudo yum install python-pip #Fedora, etc.
```
If installing from `pip` doesn't work for you, please [file an issue](https://github.com/polybuildr/petroglyph/issues) and then use the old installation instructions below instead.

### Old installation procedure

To install, first install `mistune`, `pyyaml` and `docutils`.

```bash
$ pip install mistune pyyaml docutils
```

If you don't have `pip`, first install pip using your package manager.

```bash
$ sudo apt-get install python-pip #Ubuntu, etc.
$ sudo yum install python-pip #Fedora, etc.
```

If `pip` fails to install `pyyaml` (check for the line `Successfully installed pyyaml` in the output), then you can use your package manager to install `pyyaml`.

```bash
$ sudo apt-get install python-yaml #Ubuntu, etc.
$ sudo yum install PyYAML #Fedora, etc.
```

Next, install petroglyph. Petroglyph is currently not available as a pip package, so you'll have to install it manually.

You can download a [stable release from GitHub](https://github.com/polybuildr/petroglyph/releases) or clone from master.

There is a script named `petroglyph` in the folder, this is the script you will use to set up your blog. Consider putting this in your `PATH` for ease of use.

On Linux, if using `bash`, you can add a line to your `.bashrc` to do this.

```bash
$ echo 'export PATH="/path/to/petroglyph:$PATH"' >> ~/.bashrc
$ source ~/.bashrc
```

Depending on your setup, this could be a different file, such as `~/.profile` or `~/.bash_profile`.

## Setting up a blog

1. Create a new directory for your blog.

  ```bash
  $ mkdir awesomeblog
  ```
2. Inside this new directory, run `petroglyph init` and fill in the details.

  The default theme is `monoblue`. There used to be other skins, but they're no longer there. Hopefully, I'll add them in the future. Until then, you can always edit the CSS yourself amd make a custom skin!

  ```bash
  $ cd awesomeblog
  $ petroglyph init
  Copying skin 'monoblue'...
  Creating posts directory...
  Configuring settings...
  Blog title: Awesome Blog
  Blog author: John Doe
  Blog description: The awesome blog!
  Saved configuration in config.yaml.
  Petroglyph initialized.
  ```
  At any point if you want to replace your skin or change the configuration, run `petroglyph init` again.

3. Write a new post in the `/posts` directory with a `.md` extension. (reStructuredText is also supported, give the file an `.rst` extension.) Each post's filename will be used as the post's slug when the blog is generated. Markdown support is provided using [Mistune](https://github.com/lepture/mistune). Include post metadata by writing posts as follows:

  ```
  ---
  title: The Post's Title
  tags: some-tag, another-tag
  ---
  Hello, world! **Bold**, _italics_ and `code`.

  This part will be before the 'Read more'.

  <!--more-->This part will come after the read more.
  ```
  > A post title is **required**.

  > Petroglyph uses the last modified time of a file when deciding the post publish date. If you'd like to use a custom date, add it to the metadata in the `YYYY-MM-DD` format.
  ```
  date: 2015-06-07
  ```
4. Dry run petroglyph to see if everything works fine.
  ```bash
  $ petroglyph --dry-run
  Found 1 post.
  1 new post.
  ```

5. Run petroglyph!
  ```bash
  $ petroglyph
  Found 1 post.
  1 new post.
  Generated 1 new post.
  Done.
  ```
  > If you ever want to regenerate all your pages (because of a theme change, for example), run `petroglyph --regenerate`.

6. Your blog is ready to be served in the `blog/` directory.
  ![](http://polybuildr.github.io/petroglyph/screenshot.png)
