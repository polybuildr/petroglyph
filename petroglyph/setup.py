import shutil
import os
from petroglyph import logger


def generate_config():
    logger.log("Configuring settings...")
    if os.path.exists('config.yaml'):
        logger.log(
            "The file " +
            os.path.join(os.getcwd(), "config.yaml") +
            " already exists.",
            logger.WARNING
        )
        print "Would you like to replace it? (y/n)",
        response = raw_input()
        if response.lower() != 'y':
            return
    blog_config = {}
    blog_title = raw_input("Blog title: ").strip()
    if blog_title is not '':
        blog_config['title'] = blog_title
    blog_author = raw_input("Blog author: ").strip()
    if blog_author is not '':
        blog_config['author'] = blog_author
    blog_description = raw_input("Blog description: ").strip()
    if blog_description is not '':
        blog_config['description'] = blog_description
    import yaml
    f = open('config.yaml', 'w')
    yaml.dump(blog_config, f, default_flow_style=False)
    logger.log("Saved configuration in config.yaml.", logger.SUCCESS)


def init(skin):
    skin = str(skin).strip()
    petroglyph_root = os.path.dirname(os.path.abspath(__file__))
    logger.log("Copying skin '%s'..." % skin)
    if not os.path.exists(os.path.join(petroglyph_root, 'skins', skin)):
        logger.log("Skin '%s' does not exist. Exiting." % skin, logger.ERROR)
        import sys
        sys.exit(1)
    try:
        shutil.copytree(os.path.join(petroglyph_root, 'skins', skin), 'skin')
    except OSError:
        logger.log(
            "The path " +
            os.path.join(os.getcwd(), 'skin') +
            " already exists.",
            logger.WARNING
        )
        print "Would you like to replace it? (y/n)",
        response = raw_input()
        if response.lower() == 'y':
            logger.log("Replacing skin...")
            try:
                shutil.rmtree('skin')
                shutil.copytree(os.path.join(petroglyph_root, 'skins', skin), 'skin')
            except OSError:
                logger.log("Error: Could not replace skin. Exiting.", logger.ERROR)
                exit()
    logger.log("Creating posts directory...")
    try:
        os.mkdir('posts')
    except OSError:
        logger.log("Directory exists.", logger.SUCCESS)
    logger.log("Creating pages directory...")
    try:
        os.mkdir('pages')
    except OSError:
        logger.log("Directory exists.", logger.SUCCESS)
    generate_config()
    logger.log("Petroglyph initialized.", logger.SUCCESS)
