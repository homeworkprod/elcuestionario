# -*- coding: utf-8 -*-

"""
elcuestionario.loader
~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2005-2015 Jochen Kupperschmidt
:License: GNU General Public License version 2, see LICENSE for details.
"""

import json

from .evaluation import RatingLevel
from .questionnaire import Answer, Question, Questionnaire


def load(f):
    """Load questionnaire and rating levels from a file-like object."""
    data = json.load(f)

    questionnaire = load_questionnaire(data)
    rating_levels = load_rating_levels(data)

    return questionnaire, rating_levels


def load_questionnaire(data):
    title = _load_title(data)

    questionnaire = Questionnaire(title)

    for question, answers in _load_questions(data):
        questionnaire.add_question_with_answers(question, answers)

    return questionnaire


def _load_title(data):
    return data['title']


def _load_questions(data):
    return map(_load_question, data['questions'])


def _load_question(data):
    text = data['text']
    question = Question(text)
    answers = _load_answers(data)
    return question, answers


def _load_answers(data):
    return frozenset(map(_load_answer, data['answers']))


def _load_answer(data):
    text = data['text']
    weighting = float(data['weighting'])
    return Answer(text, weighting)


def load_rating_levels(data):
    return list(_load_rating_levels(data))


def _load_rating_levels(data):
    for rating_level in data.get('rating_levels', []):
        minimum_score = int(rating_level['minimum_score'])
        text = rating_level['text']
        yield RatingLevel(minimum_score, text)
