# -*- coding: utf-8 -*-

"""
elcuestionario.userinput
~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2005-2015 Jochen Kupperschmidt
:License: GNU General Public License version 2, see LICENSE for details.
"""

from flask import request


class UserInput(object):

    @classmethod
    def from_request(cls, questionnaire):
        user_input = cls(questionnaire.get_question_hashes())
        user_input.name = request.form.get('username')
        for question_hash, answer_hash in cls._collect_answers_for_questions():
            user_input.answer_question(question_hash, answer_hash)
        return user_input

    @staticmethod
    def _collect_answers_for_questions():
        """Examine which questions were answered and with which answer."""
        for name, value in request.form.items():
            if name.startswith('q_') and value.startswith('a_'):
                question_hash = name
                answer_hash = value
                yield question_hash, answer_hash

    def __init__(self, all_question_hashes):
        self.name = None
        self.all_question_hashes = frozenset(all_question_hashes)
        self.answers_by_question = {}

    def answer_question(self, question_hash, answer_hash):
        if question_hash not in self.all_question_hashes:
            raise KeyError(
                'Unknown question with hash "{0}".'.format(question_hash))
        self.answers_by_question[question_hash] = answer_hash

    def get_answer_hash(self, question_hash):
        return self.answers_by_question.get(question_hash, None)

    def is_question_answered(self, question):
        return question.hash in self.answers_by_question

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
