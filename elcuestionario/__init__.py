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


# configuration
QUESTIONNAIRE_FILENAME = 'data/example.json'


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
    username = request.form['username']

    output = {
        'questionnaire': questionnaire,
        'username': username,
    }

    _select_answer_for_questions(questionnaire, request)

    if questionnaire.all_questions_answered:
        output['result'] = questionnaire.get_result()
        return render_template('result.html', **output)
    else:
        output['submitted'] = True
        return render_template('questionnaire.html', **output)

def _load_questionnaire():
    with app.open_resource(QUESTIONNAIRE_FILENAME) as f:
        return load_questionnaire(f)

def _select_answer_for_questions(name, questionnaire, request):
    """Examine which questions were answered and which answer was selected."""
    for name, value in request.form.items():
        if name.startswith('q_') and value.startswith('a_'):
            question_hash = name[2:]
            answer_hash = value[2:]
            questionnaire.select_answer_to_question(question_hash, answer_hash)
