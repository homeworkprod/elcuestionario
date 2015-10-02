#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse

from elcuestionario import create_app


DEFAULT_PORT = 5000


def parse_args():
    """Setup and apply the command line arguments parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='debug mode')

    parser.add_argument(
        '--port',
        dest='port',
        type=int,
        default=DEFAULT_PORT,
        help='the port to listen on [default: {:d}]'.format(DEFAULT_PORT),
        metavar='PORT')

    parser.add_argument('filename')

    return parser.parse_args()


def main():
    args = parse_args()

    app = create_app(args.filename)
    app.run(port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
