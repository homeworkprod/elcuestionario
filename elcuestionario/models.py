#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

from bisect import bisect_right
from collections import namedtuple
import hashlib
import xml.etree.ElementTree as ET


class ObjectWithHash(object):
    """A hash value will be stored when the caption is set."""

    def __init__(self, caption):
        self.caption = caption

    def _get_caption(self):
        return self.__caption

    def _set_caption(self, value):
        self.__caption = unicode(value)
        self.hash = _create_hash(self.__caption.encode('latin-1'))

    caption = property(_get_caption, _set_caption)


def _create_hash(value, length=8):
    return hashlib.sha1(value).hexdigest()[:length]


class ParsedSurveyData(object):

    def __init__(self, filename):
        self.tree = ET.parse(filename)

    def get_survey(self):
        survey = Survey(self.get_title())
        questions = map(self.get_question, self.tree.getiterator('question'))
        for question in questions:
            survey.add_question(question)
        for min_score, text in self.get_rating_levels():
            survey.add_rating_level(min_score, text)
        return survey

    def get_title(self):
        return unicode(self.tree.find('title').text)

    def get_question(self, element):
        caption = unicode(element.get('caption'))
        question = Question(caption)
        answers = map(self.get_answer, element.getiterator('answer'))
        for answer in answers:
            question.add_answer(answer)
        return question

    def get_answer(self, element):
        caption = unicode(element.get('caption'))
        weighting = float(element.get('weighting'))
        return Answer(caption, weighting)

    def get_rating_levels(self):
        for element in self.tree.getiterator('rating'):
            min_score = int(element.get('minscore'))
            yield min_score, element.text


class Survey(object):
    """A set of questions, answers, selection states and rating levels."""

    def __init__(self, title):
        self.title = title
        self._questions = {}
        self.rating_levels = {}

    @classmethod
    def from_file(cls, filename):
        """Create a survey from XML data read from a file."""
        return ParsedSurveyData(filename).get_survey()

    def __str__(self):
        return '<%s, %d questions, %d rating levels>' \
            % (self.__class__.__name__, len(self.get_questions()),
                len(self.rating_levels))

    def add_question(self, question):
        self._questions[question.hash] = question

    def get_question(self, hash):
        """Return the question for the given hash."""
        return self._questions[hash]

    def get_questions(self):
        return self._questions.values()

    @property
    def all_questions_answered(self):
        return all(question.answered for question in self.get_questions())

    @property
    def total_questions_answered(self):
        """Return the number of questions that have been answered."""
        return sum(1 for question in self.get_questions() if question.answered)

    @property
    def total_questions_unanswered(self):
        """Return the number of questions that have not been answered."""
        return len(self.get_questions()) - self.total_questions_answered

    def add_rating_level(self, min_score, text):
        self.rating_levels[min_score] = text

    def calculate_score(self):
        """Calculate the score depending on the given answers."""
        assert self.all_questions_answered
        score = sum(question.selected_answer().weighting
            for question in self.get_questions())
        return float(score) / len(self.get_questions()) * 100

    def get_rating(self, score):
        """Return the rating text for the given score."""
        min_scores = sorted(self.rating_levels.keys())

        # Don't include the lowest value in the thresholds.
        thresholds = min_scores[1:]
        index = bisect_right(thresholds, score)

        ratings = list(map(self.rating_levels.get, min_scores))
        return ratings[index]

    def get_result(self):
        """Return the evaluation result."""
        score = self.calculate_score()
        rating = self.get_rating(score)
        return Result(score, rating)


Result = namedtuple('Result', 'score rating')


class Question(dict, ObjectWithHash):
    """A question with multiple answers."""

    def __init__(self, caption):
        ObjectWithHash.__init__(self, caption)

    def __str__(self):
        return '<%s, hash=%s, caption="%s", %d answers, answered=%s>' \
            % (self.__class__.__name__, self.hash,
                self.caption.encode('latin-1'),
                len(self), self.answered)

    def add_answer(self, answer):
        self[answer.hash] = answer

    def get_answer(self, hash):
        return self[hash]

    def get_answers(self):
        return self.values()

    def select_answer(self, answer):
        """Answer the question with the given answer."""
        self[answer.hash].selected = True

    def selected_answer(self):
        """Return the chosen answer."""
        return next(answer for answer in self.values() if answer.selected)

    @property
    def answered(self):
        return any(answer.selected for answer in self.values())


class Answer(ObjectWithHash):
    """An answer to a question."""

    def __init__(self, caption, weighting):
        ObjectWithHash.__init__(self, caption)
        self.weighting = weighting
        self.selected = False

    def __str__(self):
        return '<%s, hash=%s, caption="%s", weighting=%f, selected=%s>' \
            % (self.__class__.__name__, self.hash,
                self.caption.encode('latin-1'),
                self.weighting, self.selected)
