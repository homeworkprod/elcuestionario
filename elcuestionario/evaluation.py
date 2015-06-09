# -*- coding: utf-8 -*-

"""
elcuestionario.evaluation
~~~~~~~~~~~~~~~~~~~~~~~~~

:Copyright: 2005-2015 Jochen Kupperschmidt
:License: GNU General Public License version 2, see LICENSE for details.
"""

from bisect import bisect_right
from collections import namedtuple


class Evaluator(object):

    def __init__(self, rating_levels):
        self.rating_level_map = RatingLevelMap(rating_levels)

    def calculate_score(self, questionnaire, user_input):
        """Calculate the score depending on the given answers."""
        assert user_input.all_questions_answered

        questions = questionnaire.get_questions()
        weightings = self._collect_selected_answers_weightings(
            questionnaire, questions, user_input)
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
        return self.rating_level_map.get_text_for_score(score)

    def get_result(self, questionnaire, user_input):
        """Return the evaluation result."""
        score = self.calculate_score(questionnaire, user_input)
        text = self.get_rating_text(score)
        return Result(score, text)


RatingLevel = namedtuple('RatingLevel', 'minimum_score text')


Result = namedtuple('Result', 'score text')


class RatingLevelMap(object):

    def __init__(self, rating_levels):
        self.thresholds, self.ratings \
            = prepare_thresholds_and_ratings(rating_levels)

    def get_text_for_score(self, score):
        """Return the rating text for the given score."""
        if not self.ratings:
            return

        index = bisect_right(self.thresholds, score)
        return self.ratings[index]


def prepare_thresholds_and_ratings(rating_levels):
    minimum_scores_to_texts = map_minimum_scores_to_texts(rating_levels)
    minimum_scores = sorted(minimum_scores_to_texts.keys())

    # Don't include the lowest value in the thresholds.
    thresholds = minimum_scores[1:]

    ratings = list(map(minimum_scores_to_texts.get, minimum_scores))

    return thresholds, ratings


def map_minimum_scores_to_texts(rating_levels):
    """Map each rating level's minimum score to its text."""
    return {rl.minimum_score: rl.text for rl in rating_levels}
