import os
import shutil
import copy

import yaml
import htmlmin
from jinja2 import Template
from petroglyph.post import Post
from petroglyph.page import Page
from petroglyph import logger


def process_template(template_text, args):
    template = Template(template_text)
    html = template.render(args)
    if not isinstance(html, unicode):
        html = unicode(html, 'utf-8')
    return htmlmin.minify(html)


def generate(regenerate=False, dry_run=False):
    cwd = os.getcwd()
    with open(os.path.join(cwd, 'config.yaml'), 'rb') as f:
        config = yaml.safe_load(f)
    page_files = [file for file in os.listdir(os.path.join(cwd, 'pages')) if file[0] != '.']
    drafts = [file for file in os.listdir(os.path.join(cwd, 'posts')) if file[0] != '.']

    if set(drafts).intersection(page_files):
        # TODO: make error more informative
        raise ValueError("A post and a page cannot have the same file name.")

    pages = []
    for page_file in page_files:
        pages.append(Page(file=os.path.join('pages', page_file)))

    posts = []
    for draft in drafts:
        posts.append(Post(file=os.path.join(cwd, 'posts', draft)))
    skin = {}
    with open(os.path.join('skin', 'post.html'), 'rb') as f:
        skin['post'] = f.read()
    with open(os.path.join('skin', 'page.html'), 'rb') as f:
        skin['page'] = f.read()
    with open(os.path.join('skin', 'home.html')) as f:
        skin['home'] = f.read()
    with open(os.path.join('skin', 'tag.html')) as f:
        skin['tag'] = f.read()
    if not os.path.isdir('blog'):
        os.mkdir('blog')
    if os.path.exists('.petroglyph-metadata'):
        with open('.petroglyph-metadata', 'rb') as f:
            posts_meta = yaml.safe_load(f)
    else:
        posts_meta = {}

    os.chdir('blog')
    logger.log("Found %d post%s." % (len(posts), '' if len(posts) == 1 else 's'))
    logger.log("Found %d page%s." % (len(pages), '' if len(pages) == 1 else 's'))

    stats = {}
    stats['new_posts'] = 0
    stats['changed_posts'] = 0
    stats['regenerated_posts'] = 0
    stats['generated_posts'] = 0
    stats['generated_pages'] = 0
    current_posts_slugs = []
    current_pages_slugs = []

    blog = {
        'title': config['title'],
        'description': config['description'],
        'author': config['author'],
        'posts': []
    }

    posts.sort(key=lambda p: (p.get_time(), p.slug), reverse=True)

    for post in posts:
        item = {
            'title': post.title,
            'slug': post.slug,
            'tags': post.tags,
            'date': post.getmtime(),
            'peek': post.get_preview()
        }
        blog['posts'].append(item)

    for post in posts:
        current_posts_slugs.append(post.slug)
        if post.slug in posts_meta:
            post.mtime = posts_meta[post.slug]['mtime']
            new = False
        else:
            new = True
            stats['new_posts'] += 1
        if not os.path.exists(post.slug):
            os.mkdir(post.slug)
        post_hash = post.get_hash()
        if not new and post_hash != posts_meta[post.slug]['hash']:
            stats['changed_posts'] += 1
        if regenerate or new or post_hash != posts_meta[post.slug]['hash']:
            posts_meta[post.slug] = {'mtime': post.mtime, 'hash': post_hash}
            post_args = {
                'post': {
                    'title': post.title,
                    'tags': post.tags,
                    'date': post.getmtime(),
                    'content': post.get_html()
                },
                'blog': blog
            }
            post_data = copy.deepcopy(post.front_matter_data)
            post_data.update(post_args)
            if not dry_run:
                if not new:
                    stats['regenerated_posts'] += 1
                else:
                    stats['generated_posts'] += 1
                with open(os.path.join(post.slug, 'index.html'), 'wb') as post_file:
                    post_file.write(process_template(skin['post'], post_data))

    for page in pages:
        current_pages_slugs.append(page.slug)
        if not os.path.exists(page.slug):
            os.mkdir(page.slug)
        page_args = {
            'page': {
                'title': page.title,
                'content': page.get_html()
            },
            'blog': blog
        }
        page_data = copy.deepcopy(page.front_matter_data)
        page_data.update(page_args)
        if not dry_run:
            stats['generated_pages'] += 1
            with open(os.path.join(page.slug, 'index.html'), 'wb') as page_file:
                page_file.write(process_template(skin['page'], page_data))

    tag_data = {}
    for post in posts:
        for tag in post.tags:
            if tag not in tag_data:
                tag_data[tag] = []
            tag_data[tag].append({
                'title': post.title,
                'tags': post.tags,
                'date': post.getmtime(),
                'peek': post.get_preview(),
                'slug': post.slug
            })
    home_args = {
        'blog': blog
    }
    tag_args = {
        'blog': blog
    }
    if stats['new_posts']:
        logger.log(
            "%s new post%s." % (
                stats['new_posts'],
                '' if stats['new_posts'] == 1 else 's'
            ),
            logger.SUCCESS
        )
    if stats['changed_posts']:
        logger.log(
            "%s changed post%s." % (
                stats['changed_posts'],
                '' if stats['changed_posts'] == 1 else 's'
            ),
            logger.WARNING
        )
    if not dry_run and (regenerate or stats['new_posts'] + stats['changed_posts'] > 0):
        with open('index.html', 'wb') as f:
            f.write(process_template(skin['home'], home_args))
        if not os.path.isdir('tag'):
            os.mkdir('tag')
        for tag in tag_data:
            if not os.path.isdir(os.path.join('tag', tag)):
                os.mkdir(os.path.join('tag', tag))
            tag_args.update(
                {
                    'tag': tag,
                    'posts': tag_data[tag]
                }
            )
            with open(os.path.join('tag', tag, 'index.html'), 'wb') as f:
                f.write(process_template(skin['tag'], tag_args))

    deleted_posts = set(posts_meta).difference(current_posts_slugs)
    stats['deleted_posts'] = len(deleted_posts)

    if stats['deleted_posts']:
        logger.log(
            "%s deleted post%s." % (
                stats['deleted_posts'],
                '' if stats['deleted_posts'] == 1 else 's'
            ),
            logger.ERROR
        )

    if stats['new_posts'] + stats['changed_posts'] + stats['deleted_posts'] == 0:
        logger.log("No changes to make to posts.")

    if not dry_run:
        for deleted_post in deleted_posts:
            del posts_meta[deleted_post]
            try:
                shutil.rmtree(deleted_post)
            except:
                logger.log("Failed to delete '%s'." % deleted_post, logger.ERROR)
        if stats['deleted_posts']:
            logger.log(
                "Deleted %s old post%s." % (
                    stats['deleted_posts'],
                    '' if stats['deleted_posts'] == 1 else 's'
                ),
                logger.SUCCESS
            )
    os.chdir(os.pardir)
    if not dry_run:
        with open('.petroglyph-metadata', 'wb') as f:
            yaml.dump(posts_meta, f)
        paths = os.listdir('skin')
        for path in paths:
            if os.path.isdir(os.path.join('skin', path)):
                if os.path.exists(os.path.join('blog', path)):
                    shutil.rmtree(os.path.join('blog', path))
                shutil.copytree(os.path.join('skin', path), os.path.join('blog', path))
        if stats['generated_pages']:
            logger.log(
                "Generated %s page%s." % (
                    stats['generated_pages'],
                    '' if stats['generated_pages'] == 1 else 's'
                ),
                logger.SUCCESS
            )
    if ((stats['generated_posts'] or stats['regenerated_posts'] or stats['deleted_posts']) and
            not dry_run):
        if stats['generated_posts']:
            logger.log(
                "Generated %s new post%s." % (
                    stats['generated_posts'],
                    '' if stats['generated_posts'] == 1 else 's'
                ),
                logger.SUCCESS
            )
        if stats['regenerated_posts']:
            logger.log(
                "Regenerated %s post%s." % (
                    stats['regenerated_posts'],
                    '' if stats['regenerated_posts'] == 1 else 's'
                ),
                logger.SUCCESS
            )
    if not dry_run:
        logger.log("Done.", logger.SUCCESS)
