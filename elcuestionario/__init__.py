# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

from random import shuffle

from flask import Flask, render_template

from .loader import load_questionnaire
from .models import UserInput


app = Flask(__name__)


@app.template_filter()
def shuffled(iterable):
    """Return a shuffled copy of the given iterable."""
    l = list(iterable)
    shuffle(l)
    return l


@app.route('/', methods=['GET'])
def view():
    questionnaire = _load_questionnaire()

    output = {
        'questionnaire': questionnaire,
        'submitted': False,
    }

    return render_template('questionnaire.html', **output)

@app.route('/', methods=['POST'])
def evaluate():
    questionnaire = _load_questionnaire()

    user_input = UserInput.from_request(questionnaire)

    output = {
        'questionnaire': questionnaire,
        'username': user_input.name,
    }

    if user_input.all_questions_answered:
        output['result'] = questionnaire.get_result(user_input)
        return render_template('result.html', **output)
    else:
        output['submitted'] = True
        output['user_input'] = user_input
        return render_template('questionnaire.html', **output)

def _load_questionnaire():
    with app.open_resource(_get_questionnaire_filename()) as f:
        return load_questionnaire(f)

def _get_questionnaire_filename():
    filename = app.config.get('QUESTIONNAIRE_FILENAME', None)
    if filename is None:
        raise Exception('Please provide the questionnaire filename as value '
            'for the key \'QUESTIONNAIRE_FILENAME\'.')
    return filename
