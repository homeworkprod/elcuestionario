# -*- coding: utf-8 -*-

from unittest import TestCase

from nose2.tools import params

from survey import FILE_SURVEY, Survey


class SurveyTestCase(TestCase):

    @params(
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
        survey = self._create_survey()
        actual = survey.get_rating(score)
        self.assertEqual(actual, expected)

    def _create_survey(self):
        survey = Survey('Test')

        survey.add_rating_level(0, 'worst')
        survey.add_rating_level(30, 'oh-oh')
        survey.add_rating_level(60, 'OK-ish')
        survey.add_rating_level(90, 'great')
        survey.add_rating_level(100, 'over the top')

        return survey
