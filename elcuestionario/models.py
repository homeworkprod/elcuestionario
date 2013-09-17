# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

from bisect import bisect_right
from collections import defaultdict, namedtuple
import hashlib


class Questionnaire(object):
    """A set of questions, answers, selection states and rating levels."""

    def __init__(self, title):
        self.title = title
        self._questions = []
        self._question_answers = defaultdict(dict)
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


class Evaluator(object):

    def __init__(self, rating_levels):
        self.rating_levels = rating_levels

    def calculate_score(self, questionnaire, user_input):
        """Calculate the score depending on the given answers."""
        assert user_input.all_questions_answered

        questions = questionnaire.get_questions()
        weightings = self._collect_selected_answers_weightings(questionnaire,
            questions, user_input)
        score = sum(weightings)
        return float(score) / len(questions) * 100

    def _collect_selected_answers_weightings(self, questionnaire, questions,
            user_input):
        for question in questions:
            answer_hash = user_input.get_answer_hash(question.hash)
            answer = questionnaire.get_answer_by_hash(question, answer_hash)
            yield answer.weighting

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

    def get_result(self, questionnaire, user_input):
        """Return the evaluation result."""
        score = self.calculate_score(questionnaire, user_input)
        text = self.get_rating_text(score)
        return Result(score, text)


RatingLevel = namedtuple('RatingLevel', 'minimum_score text')

Result = namedtuple('Result', 'score text')


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
