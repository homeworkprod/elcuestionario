# -*- coding: utf-8 -*-

"""
Tests for El Cuestionario
=========================


Requirements
------------

- nose2_ (tested with version 0.4.7)


Installation
------------

Install nose2_:

.. code:: sh

    $ pip install nose2


Usage
-----

Run the tests (attention: do *not* specify the `.py` extension, just the
module name!):

.. code:: sh

    $ nose2 test_elcuestionario


.. _nose2: https://github.com/nose-devs/nose2
"""

from unittest import TestCase

from nose2.tools import params

from elcuestionario.loader import _load_survey
from elcuestionario.models import Answer, Evaluator, Question, RatingLevel, Survey


class AbstractLoaderTestCase(TestCase):

    def setUp(self):
        data = self._get_data_string()
        survey = _load_survey(data)

        self.questions = survey.get_questions()
        self.rating_levels = survey.rating_levels

    def assertAnswersEqual(self, question_index, expected):
        answers = self._get_answers(question_index)
        texts = self._get_answer_texts(answers)
        self.assertEqual(texts, expected)

    def _get_answers(self, question_index):
        return self.questions[question_index].get_answers()

    def _get_answer_texts(self, answers):
        return set(answer.text for answer in answers)


class LoaderTestCase(AbstractLoaderTestCase):

    def _get_data_string(self):
        return u'''<?xml version="1.0" encoding="UTF-8"?>
<survey>
    <title>How strange are you?</title>
    <questions>
        <question text="question 1">
            <answer text="answer 1.1" weighting="0.0"/>
            <answer text="answer 1.2" weighting="0.5"/>
            <answer text="answer 1.3" weighting="1.0"/>
        </question>
        <question text="question 2">
            <answer text="answer 2.1" weighting="0.0"/>
            <answer text="answer 2.2" weighting="0.25"/>
            <answer text="answer 2.3" weighting="0.5"/>
            <answer text="answer 2.4" weighting="0.75"/>
            <answer text="answer 2.5" weighting="1.0"/>
        </question>
    </questions>
    <ratings>
        <rating minscore="0">bad</rating>
        <rating minscore="50">okay</rating>
        <rating minscore="80">good</rating>
    </ratings>
</survey>
'''

    def test_questions(self):
        self.assertEqual(len(self.questions), 2)
        self.assertEqual(self.questions[0].text, 'question 1')
        self.assertEqual(self.questions[1].text, 'question 2')

    def test_answers(self):
        self.assertAnswersEqual(0, set([
            'answer 1.1',
            'answer 1.2',
            'answer 1.3',
        ]))

        self.assertAnswersEqual(1, set([
            'answer 2.1',
            'answer 2.2',
            'answer 2.3',
            'answer 2.4',
            'answer 2.5',
        ]))

    def test_rating_levels(self):
        self.assertEqual(self.rating_levels, [
            RatingLevel( 0, 'bad'),
            RatingLevel(50, 'okay'),
            RatingLevel(80, 'good'),
        ])


class UnicodeLoaderTestCase(AbstractLoaderTestCase):

    def _get_data_string(self):
        return u'''<?xml version="1.0" encoding="UTF-8"?>
<survey>
    <title>Frägebögen</title>
    <questions>
        <question text="Farbtöne">
            <answer text="weiß" weighting="0.0"/>
            <answer text="grün" weighting="0.0"/>
            <answer text="rötlich" weighting="0.0"/>
        </question>
    </questions>
    <ratings>
        <rating minscore="0">großartig</rating>
    </ratings>
</survey>
'''

    def test_questions(self):
        self.assertEqual(self.questions[0].text, u'Farbtöne')

    def test_answers(self):
        self.assertAnswersEqual(0, set([
            u'weiß',
            u'grün',
            u'rötlich',
        ]))

    def test_rating_levels(self):
        self.assertEqual(self.rating_levels, [
            RatingLevel( 0, u'großartig'),
        ])


class QuestionTestCase(TestCase):

    def setUp(self):
        self.question = Question('some question')

        self.answer1 = Answer('yes', 1.0)
        self.answer2 = Answer('maybe', 0.5)
        self.answer3 = Answer('no', 0.0)

        self.question.add_answer(self.answer1)
        self.question.add_answer(self.answer2)
        self.question.add_answer(self.answer3)

    def test_answered(self):
        self.assertEquals(self.question.answered, False)
        self.question.select_answer(self.answer3)
        self.assertEquals(self.question.answered, True)


class RatingTestCase(TestCase):

    def setUp(self):
        rating_levels = [RatingLevel(minimum_score, text)
            for minimum_score, text in [
                (0, 'worst'),
                (30, 'oh-oh'),
                (60, 'OK-ish'),
                (90, 'great'),
                (100, 'over the top'),
            ]]

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
