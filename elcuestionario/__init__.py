# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

from random import shuffle

from flask import Flask, render_template, request

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

    user_input = UserInput(questionnaire.get_question_hashes())

    output = {
        'questionnaire': questionnaire,
        'submitted': False,
        'user_input': user_input,
    }

    return render_template('questionnaire.html', **output)

@app.route('/', methods=['POST'])
def evaluate():
    questionnaire = _load_questionnaire()
    username = request.form['username']

    user_input = UserInput(questionnaire.get_question_hashes())
    user_input.name = username
    _select_answers_for_questions(user_input, questionnaire, request)

    output = {
        'questionnaire': questionnaire,
        'username': username,
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

def _select_answers_for_questions(user_input, questionnaire, request):
    """Examine which questions were answered and which answer was selected."""
    for name, value in request.form.items():
        if name.startswith('q_') and value.startswith('a_'):
            question_hash = name[2:]
            answer_hash = value[2:]
            user_input.answer_question(question_hash, answer_hash)
