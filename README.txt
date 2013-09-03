Rate Yourself

Copyright (c) 2005, 2006 Jochen Kupperschmidt <webmaster@nwsnet.de>
Released under the terms of the GNU General Public License
  _                               _
 | |_ ___ _____ ___ _ _ _ ___ ___| |_
 |   | . |     | ._| | | | . |  _| . /
 |_|_|___|_|_|_|___|_____|___|_| |_|_\
   http://homework.nwsnet.de/

'Rate Yourself' is a web framework for building surveys like
'How cool/geeky/whatever are you?'. All survey-specific data (questions, their
answers and score ratings) is read from a single file containing XML data. The
questions and answers are presented to the user in random order. When all
questions are answered, the user's score is calculated based on the answers'
weight (as specified in the data file) and presented with a suitable comment.

Requirements:
  - Python 2.3 (http://www.python.org/), tested with 2.3.5
  - ElementTree (http://effbot.org/zone/element-index.htm), tested with 1.2.6
  - Kid (http://kid.lesscode.org/), tested with 0.9.1

Installation:
  - Make sure the required software is installed.
  - Note: ElementTree and Kid are pure Python packages and can be installed
    especially on webspace-only hostings by simply uploading them.
  - Make those packages available to your script. If they are not already in
    your PYTHONPATH, set the path in the imports section of the main script.
  - The main script has to be executable (e.g. through 'chmod +x index.py').
  - Take a look at 'data/example.xml' on how a survey is made up. Just copy it,
    adjust its content and change the FILE_SURVEY variable in the main script
    accordingly.
