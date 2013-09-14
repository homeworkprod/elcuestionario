# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

import codecs
import xml.etree.ElementTree as ET

from .models import Answer, Question, RatingLevel, Survey


def load_survey(filename):
    """Load a survey from the specified file."""
    with codecs.open(filename, encoding='utf-8') as f:
        data = f.read()
    return _load_survey(data)

def _load_survey(data):
    """Load a survey from the data string."""
    tree = ET.fromstring(data.encode('utf-8'))

    title = _get_title(tree)

    survey = Survey(title)

    for question in _get_questions(tree):
        survey.add_question(question)

    for rating_level in _get_rating_levels(tree):
        survey.add_rating_level(rating_level)

    return survey

def _get_title(tree):
    return unicode(tree.find('title').text)

def _get_questions(tree):
    return map(_get_question, tree.getiterator('question'))

def _get_question(element):
    caption = unicode(element.get('caption'))
    question = Question(caption)
    for answer in _get_answers(element):
        question.add_answer(answer)
    return question

def _get_answers(element):
    return map(_get_answer, element.getiterator('answer'))

def _get_answer(element):
    caption = unicode(element.get('caption'))
    weighting = float(element.get('weighting'))
    return Answer(caption, weighting)

def _get_rating_levels(tree):
    for element in tree.getiterator('rating'):
        minimum_score = int(element.get('minscore'))
        text = element.text
        yield RatingLevel(minimum_score, text)
