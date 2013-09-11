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

from .loader import load_survey


# configuration
SURVEY_FILENAME = 'elcuestionario/data/example.xml'


app = Flask(__name__)


@app.template_filter()
def shuffled(iterable):
    """Return a shuffled copy of the given iterable."""
    l = list(iterable)
    shuffle(l)
    return l


@app.route('/', methods=['GET'])
def view():
    survey = _load_survey()

    output = {
        'survey': survey,
        'submitted': False,
    }

    return render_template('questionnaire.html', **output)

@app.route('/', methods=['POST'])
def evaluate():
    survey = _load_survey()
    username = request.form['username']

    output = {
        'survey': survey,
        'username': username,
    }

    _select_answer_for_questions(survey, request)

    if survey.all_questions_answered:
        output['result'] = survey.get_result()
        return render_template('result.html', **output)
    else:
        output['submitted'] = True
        return render_template('questionnaire.html', **output)

def _load_survey():
    return load_survey(SURVEY_FILENAME)

def _select_answer_for_questions(survey, request):
    """Examine which questions were answered and which answer was selected."""
    for name, value in request.form.items():
        if name.startswith('q_') and value.startswith('a_'):
            question_hash = name[2:]
            answer_hash = value[2:]
            _select_answer_for_question(survey, question_hash, answer_hash)

def _select_answer_for_question(survey, question_hash, answer_hash):
    """Lookup the question and answer for the given hashes,
    respectively, and select the answer for the question.
    """
    question = survey.get_question(question_hash)
    answer = question.get_answer(answer_hash)
    question.select_answer(answer)
