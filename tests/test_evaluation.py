# -*- coding: utf-8 -*-

from unittest import TestCase

from nose2.tools import params

from elcuestionario.evaluation import Evaluator, RatingLevel

from .helpers import AbstractTestCase


class RatingTestCase(TestCase):

    def setUp(self):
        rating_levels = [
            RatingLevel(minimum_score, text)
            for minimum_score, text in [
                (  0, 'worst'),
                ( 30, 'oh-oh'),
                ( 60, 'OK-ish'),
                ( 90, 'great'),
                (100, 'over the top'),
            ]
        ]

        self.evaluator = Evaluator(rating_levels)

    @params(
        ( -2.3, 'worst'),
        (  0.0, 'worst'),
        (  4.2, 'worst'),
        ( 29.3, 'worst'),
        ( 30.0, 'oh-oh'),
        ( 59.5, 'oh-oh'),
        ( 60.0, 'OK-ish'),
        ( 89.7, 'OK-ish'),
        ( 90.0, 'great'),
        ( 99.9, 'great'),
        (100.0, 'over the top'),
        (111.1, 'over the top'),
    )
    def test_get_rating(self, score, expected):
        actual = self.evaluator.get_rating_text(score)
        self.assertEqual(actual, expected)


class WithoutRatingTextsTestCase(AbstractTestCase):

    def _get_data_string(self):
        return u'''{
    "title": "some title",
    "questions": [
        {
            "text": "some question",
            "answers": [
                { "text": "some answer", "weighting": 1.0 }
            ]
        }
    ]
}
'''

    def test_result_without_text(self):
        score = 0.5
        actual = self.evaluator.get_rating_text(score)
        self.assertEqual(actual, None)
