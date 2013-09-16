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


class Survey(object):
    """A set of questions, answers, selection states and rating levels."""

    def __init__(self, title):
        self.title = title
        self._questions = []
        self.rating_levels = []

    def __str__(self):
        return '<%s, %d questions, %d rating levels>' \
            % (self.__class__.__name__, len(self.get_questions()),
                len(self.rating_levels))

    def add_question(self, question):
        self._questions.append(question)

    def get_question(self, hash):
        """Return the question for the given hash."""
        for question in self._questions:
            if question.hash == hash:
                return question

    def get_questions(self):
        return self._questions

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

    def add_rating_level(self, rating_level):
        self.rating_levels.append(rating_level)

    def get_result(self):
        evaluator = Evaluator(self.rating_levels)
        return evaluator.get_result(self)


class Evaluator(object):

    def __init__(self, rating_levels):
        self.rating_levels = rating_levels

    def calculate_score(self, survey):
        """Calculate the score depending on the given answers."""
        assert survey.all_questions_answered
        questions = survey.get_questions()
        score = sum(question.selected_answer().weighting
            for question in questions)
        return float(score) / len(questions) * 100

    def get_rating_text(self, score):
        """Return the rating text for the given score."""
        minimum_scores_to_texts = dict((rl.minimum_score, rl.text)
            for rl in self.rating_levels)

        minimum_scores = sorted(minimum_scores_to_texts.keys())

        # Don't include the lowest value in the thresholds.
        thresholds = minimum_scores[1:]
        index = bisect_right(thresholds, score)

        ratings = list(map(minimum_scores_to_texts.get, minimum_scores))
        return ratings[index]

    def get_result(self, survey):
        """Return the evaluation result."""
        score = self.calculate_score(survey)
        text = self.get_rating_text(score)
        return Result(score, text)


RatingLevel = namedtuple('RatingLevel', 'minimum_score text')

Result = namedtuple('Result', 'score text')


class Question(object):
    """A question with multiple answers."""

    def __init__(self, text):
        self.text = text
        self.hash = _create_hash(self.text.encode('latin-1'))
        self.answers = {}
        self._selected_answer_hash = None

    def __str__(self):
        return '<%s, hash=%s, text="%s", %d answers, answered=%s>' \
            % (self.__class__.__name__, self.hash,
                self.text.encode('latin-1'),
                len(self.answers), self.answered)

    def add_answer(self, answer):
        self.answers[answer.hash] = answer

    def get_answer(self, hash):
        return self.answers[hash]

    def get_answers(self):
        return self.answers.values()

    def select_answer(self, answer):
        """Answer the question with the given answer."""
        self._selected_answer_hash = answer.hash

    def selected_answer(self):
        """Return the chosen answer."""
        return next(answer for answer in self.answers.values()
            if answer.hash == self._selected_answer_hash)

    @property
    def answered(self):
        return self._selected_answer_hash is not None

    def is_answer_selected(self, answer):
        return answer.hash == self._selected_answer_hash


class Answer(namedtuple('Answer', 'text weighting hash')):

    def __new__(cls, text, weighting):
        hash = _create_hash(text.encode('latin-1'))
        return super(Answer, cls).__new__(cls, text, weighting, hash)


def _create_hash(value, length=8):
    return hashlib.sha1(value).hexdigest()[:length]
