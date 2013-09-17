# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

from collections import defaultdict, namedtuple
import hashlib

from flask import request

from .evaluation import Evaluator


class Questionnaire(object):
    """A set of questions, answers, selection states and rating levels."""

    def __init__(self, title):
        self.title = title
        self._questions = []
        self._question_answers = defaultdict(dict)
        self.rating_levels = []

    def add_question(self, question):
        self._questions.append(question)

    def get_question(self, hash):
        """Return the question for the given hash."""
        for question in self._questions:
            if question.hash == hash:
                return question

    def get_questions(self):
        return self._questions

    def get_question_hashes(self):
        return (question.hash for question in self.get_questions())

    def add_answer_for_question(self, question, answer):
        self._question_answers[question.hash][answer.hash] = answer

    def get_answers_for_question(self, question):
        return self._question_answers[question.hash].values()

    def get_answer_by_hash(self, question, answer_hash):
        return self._question_answers[question.hash][answer_hash]

    def select_answer_to_question(self, question_hash, answer_hash):
        """Answer the referenced question with the referenced answer."""
        question = self.get_question(question_hash)
        answer = self.get_answer_by_hash(question, answer_hash)
        question.select_answer(answer)

    def add_rating_level(self, rating_level):
        self.rating_levels.append(rating_level)

    def get_result(self, user_input):
        evaluator = Evaluator(self.rating_levels)
        return evaluator.get_result(self, user_input)


class Question(namedtuple('Question', 'text hash')):

    def __new__(cls, text):
        hash = _create_hash(text.encode('latin-1'))
        return super(Question, cls).__new__(cls, text, hash)


class Answer(namedtuple('Answer', 'text weighting hash')):

    def __new__(cls, text, weighting):
        hash = _create_hash(text.encode('latin-1'))
        return super(Answer, cls).__new__(cls, text, weighting, hash)


def _create_hash(value, length=8):
    return hashlib.sha1(value).hexdigest()[:length]


class UserInput(object):

    @classmethod
    def from_request(cls, questionnaire):
        user_input = cls(questionnaire.get_question_hashes())
        user_input.name = request.form['username']
        for question_hash, answer_hash in cls._collect_answers_for_questions():
            user_input.answer_question(question_hash, answer_hash)
        return user_input

    @staticmethod
    def _collect_answers_for_questions():
        """Examine which questions were answered and which answer was selected."""
        for name, value in request.form.items():
            if name.startswith('q_') and value.startswith('a_'):
                question_hash = name[2:]
                answer_hash = value[2:]
                yield question_hash, answer_hash

    def __init__(self, all_question_hashes):
        self.name = None
        self.all_question_hashes = frozenset(all_question_hashes)
        self.answers_by_question = {}

    def answer_question(self, question_hash, answer_hash):
        if question_hash not in self.all_question_hashes:
            raise KeyError('Unknown question with hash "%s".' % question_hash)
        self.answers_by_question[question_hash] = answer_hash

    def get_answer_hash(self, question_hash):
        return self.answers_by_question.get(question_hash, None)

    def is_answer_selected(self, question, answer):
        found_answer_hash = self.get_answer_hash(question.hash)
        return (found_answer_hash is not None) and \
            (found_answer_hash == answer.hash)

    @property
    def questions_total(self):
        return len(self.all_question_hashes)

    @property
    def all_questions_answered(self):
        answered_questions_hashes = frozenset(self.answers_by_question.keys())
        return answered_questions_hashes.issuperset(self.all_question_hashes)

    @property
    def total_questions_answered(self):
        """Return the number of questions that have been answered."""
        return len(self.answers_by_question.keys())

    @property
    def total_questions_unanswered(self):
        """Return the number of questions that have not been answered."""
        return self.questions_total - self.total_questions_answered
