# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

import codecs
import json

from .models import Answer, Question, RatingLevel, Survey


def load_survey(filename):
    """Load a survey from the specified file."""
    with codecs.open(filename, encoding='utf-8') as f:
        data = f.read()
    return _load_survey(data)

def _load_survey(data):
    """Load a survey from the data string."""
    data = json.loads(data)

    title = _get_title(data)

    survey = Survey(title)

    for question in _get_questions(data):
        survey.add_question(question)

    for rating_level in _get_rating_levels(data):
        survey.add_rating_level(rating_level)

    return survey

def _get_title(data):
    return data['title']

def _get_questions(data):
    return map(_get_question, data['questions'])

def _get_question(data):
    text = data['text']
    question = Question(text)
    for answer in _get_answers(data):
        question.add_answer(answer)
    return question

def _get_answers(data):
    return map(_get_answer, data['answers'])

def _get_answer(data):
    text = data['text']
    weighting = float(data['weighting'])
    return Answer(text, weighting)

def _get_rating_levels(data):
    for rating_level in data['rating_levels']:
        minimum_score = int(rating_level['minimum_score'])
        text = rating_level['text']
        yield RatingLevel(minimum_score, text)
