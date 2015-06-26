#!/usr/bin/env python
import argparse
import os
from petroglyph import logger

parser = argparse.ArgumentParser()
parser.add_argument("command", nargs="?")
parser.add_argument("--regenerate", action='store_true', help="force regeneration of all posts")
parser.add_argument("--dry-run", action='store_true', help="perform only a dry run")
parser.add_argument("--skin", default="monoblue", help="specify the skin to be used")

args = parser.parse_args()

def init():
    from petroglyph import setup
    setup.init(args.skin)

if args.command is None:
    args.command = 'generate'

if args.command == 'init':
    init()

elif args.command == 'generate':
    if not os.path.exists('config.yaml'):
        logger.log("Petroglyph has not been initialized.", logger.WARNING)
        print "Would you like to initialize it now? (y/n)",
        response = raw_input()
        if response == 'y':
            init()
        else:
            logger.log("Aborting.", logger.ERROR)
    else:
        from petroglyph import generator
        generator.generate(args.regenerate, args.dry_run)
else:
    logger.log("Invalid command '%s'." % args.command, logger.ERROR)
