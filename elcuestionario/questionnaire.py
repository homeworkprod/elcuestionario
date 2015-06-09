# -*- coding: utf-8 -*-

"""
elcuestionario.questionnaire
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2005-2015 Jochen Kupperschmidt
:License: GNU General Public License version 2, see LICENSE for details.
"""

from collections import defaultdict, namedtuple
import hashlib


class Questionnaire(object):
    """A set of questions, answers, selection states and rating levels."""

    def __init__(self, title):
        self.title = title
        self._questions = []
        self._question_answers = defaultdict(dict)

    def add_question_with_answers(self, question, answers):
        self._questions.append(question)
        for answer in answers:
            self._question_answers[question.hash][answer.hash] = answer

    def get_question(self, question_hash):
        """Return the question for the given hash."""
        for question in self._questions:
            if question.hash == question_hash:
                return question

    def get_questions(self):
        return self._questions

    def get_question_hashes(self):
        return (question.hash for question in self.get_questions())

    def get_answers_for_question(self, question):
        return self._question_answers[question.hash].values()

    def get_answer_by_hash(self, question, answer_hash):
        return self._question_answers[question.hash][answer_hash]


class Question(namedtuple('Question', 'text hash')):

    def __new__(cls, text):
        question_hash = 'q_' + _create_hash(text.encode('utf-8'))
        return super(Question, cls).__new__(cls, text, question_hash)


class Answer(namedtuple('Answer', 'text weighting hash')):

    def __new__(cls, text, weighting):
        answer_hash = 'a_' + _create_hash(text.encode('utf-8'))
        return super(Answer, cls).__new__(cls, text, weighting, answer_hash)


def _create_hash(value, length=8):
    return hashlib.sha1(value).hexdigest()[:length]
