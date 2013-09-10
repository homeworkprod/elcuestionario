# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

import xml.etree.ElementTree as ET

from .models import Answer, Question, Survey


def load_survey(filename):
    """Load a survey from the specified XML file."""
    tree = ET.parse(filename)

    title = _get_title(tree)

    survey = Survey(title)

    for question in _get_questions(tree):
        survey.add_question(question)

    for min_score, text in _get_rating_levels(tree):
        survey.add_rating_level(min_score, text)

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
        min_score = int(element.get('minscore'))
        yield min_score, element.text
