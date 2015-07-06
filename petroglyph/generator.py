import os
import shutil
import re
import copy

import yaml
from petroglyph.post import Post
from petroglyph import logger


def process_template(template, args):
    placeholders = set(re.findall('{{([a-zA-Z][a-zA-Z0-9_-]*)}}', template))
    for placeholder in placeholders:
        if placeholder in args:
            template = template.replace('{{' + placeholder + '}}', str(args[placeholder]))
    return template


def generate(regenerate=False, dry_run=False):
    cwd = os.getcwd()
    with open(os.path.join(cwd, 'config.yaml'), 'rb') as f:
        config = yaml.safe_load(f)
    drafts = [file for file in os.listdir(os.path.join(cwd, 'posts')) if file[0] != '.']
    posts = []
    for draft in drafts:
        posts.append(Post(file=os.path.join('posts', draft)))
    skin = {}
    with open(os.path.join('skin', 'post.html'), 'rb') as f:
        skin['post'] = f.read()
    with open(os.path.join('skin', 'post-peek.html'), 'rb') as f:
        skin['post-peek'] = f.read()
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
    post_previews_text = []
    os.chdir('blog')
    logger.log("Found %d post%s." % (len(posts), '' if len(posts) == 1 else 's'))
    stats = {}
    stats['new_posts'] = 0
    stats['changed_posts'] = 0
    stats['regenerated_posts'] = 0
    stats['generated_posts'] = 0
    current_posts_slugs = []

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
                'title': post.title,
                'tags': ''.join(
                    ['<a href="../tag/' + tag + '" class="tag">#' + tag + '</a>'
                        for tag in post.tags]
                ),
                'blog_title': config['title'],
                'date': post.getmtime(),
                'content': post.get_html()
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

    posts.sort(key=lambda p: (p.get_time(), p.slug), reverse=True)
    tag_data = {}
    for post in posts:
        post_peek_args = {
            'slug': post.slug,
            'title': post.title,
            'date': post.getmtime(),
            'peek': post.get_preview(),
            'tags': ''.join(
                ['<a href="tag/' + tag + '" class="tag">#' + tag + '</a>'
                    for tag in post.tags]
            )
        }
        post_peek_data = copy.deepcopy(post.front_matter_data)
        post_peek_data.update(post_peek_args)
        post_previews_text.append(process_template(skin['post-peek'], post_peek_data))
        post_peek_data.update({
            'tags': ''.join(
                ['<a href="../../tag/' + tag + '" class="tag">#' + tag + '</a>'
                    for tag in post.tags]
            ),
            'slug': '../../' + post.slug
        })
        for tag in post.tags:
            if tag not in tag_data:
                tag_data[tag] = []
            tag_data[tag].append(process_template(skin['post-peek'], post_peek_data))
    home_args = {
        'title': config['title'],
        'author': config['author'],
        'description': config['description'],
        'posts': "\n".join(post_previews_text)
    }
    tag_args = {
        'title': config['title'],
        'author': config['author'],
        'description': config['description'],
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
                    'tag': '#' + tag,
                    'posts': "\n".join(tag_data[tag])
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
        logger.log("No changes to make.")

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
    if ((stats['generated_posts'] or stats['regenerated_posts'] or stats['deleted_posts'])
            and not dry_run):
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
