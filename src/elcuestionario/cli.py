"""
elcuestionario.cli
~~~~~~~~~~~~~~~~~~

Command line interface to start the application

:Copyright: 2005-2021 Jochen Kupperschmidt
:License: GNU General Public License version 2, see LICENSE for details.
"""

import argparse
from pathlib import Path

from .app import create_app


DEFAULT_PORT = 5000


def parse_args():
    """Setup and apply the command line arguments parser."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--debug',
        dest='debug',
        action='store_true',
        default=False,
        help='debug mode',
    )

    parser.add_argument(
        '--port',
        dest='port',
        type=int,
        default=DEFAULT_PORT,
        help=f'the port to listen on [default: {DEFAULT_PORT:d}]',
        metavar='PORT',
    )

    parser.add_argument('filename')

    return parser.parse_args()


def main():
    args = parse_args()

    app = create_app(Path(args.filename))
    app.run(port=args.port, debug=args.debug)
