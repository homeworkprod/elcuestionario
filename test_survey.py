# -*- coding: utf-8 -*-

"""
Tests for Rate Yourself
=======================


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

    $ nose2 test_survey


.. _nose2: https://github.com/nose-devs/nose2
"""

from io import StringIO
from unittest import TestCase

from nose2.tools import params

from survey import Answer, Question, Survey


class XmlLoaderTestCase(TestCase):

    def setUp(self):
        f = self._create_file()
        self.survey = Survey.from_file(f)

    def _create_file(self):
        return StringIO(
u'''<?xml version="1.0" encoding="UTF-8"?>
<survey>
    <title>How strange are you?</title>
    <questions>
        <question caption="question 1">
            <answer caption="answer 1.1" weighting="0.0"/>
            <answer caption="answer 1.2" weighting="0.5"/>
            <answer caption="answer 1.3" weighting="1.0"/>
        </question>
        <question caption="question 2">
            <answer caption="answer 2.1" weighting="0.0"/>
            <answer caption="answer 2.2" weighting="0.25"/>
            <answer caption="answer 2.3" weighting="0.5"/>
            <answer caption="answer 2.4" weighting="0.75"/>
            <answer caption="answer 2.5" weighting="1.0"/>
        </question>
    </questions>
    <ratings>
        <rating minscore="0">bad</rating>
        <rating minscore="50">okay</rating>
        <rating minscore="80">good</rating>
    </ratings>
</survey>
''')

    def test_questions(self):
        questions = self.survey.get_questions()
        self.assertEqual(len(questions), 2)
        self.assertEqual(questions[0].caption, 'question 1')
        self.assertEqual(questions[1].caption, 'question 2')

    def test_answers(self):
        questions = self.survey.get_questions()

        question1_answers = questions[0].get_answers()
        self.assertEqual(len(question1_answers), 3)
        question1_answer_captions = set(
            answer.caption for answer in question1_answers)
        self.assertEqual(question1_answer_captions, set([
            'answer 1.1',
            'answer 1.2',
            'answer 1.3',
        ]))

        question2_answers = questions[1].get_answers()
        self.assertEqual(len(question2_answers), 5)
        question2_answer_captions = set(
            answer.caption for answer in question2_answers)
        self.assertEqual(question2_answer_captions, set([
            'answer 2.1',
            'answer 2.2',
            'answer 2.3',
            'answer 2.4',
            'answer 2.5',
        ]))

    def test_ratings(self):
        self.assertEqual(self.survey.rating_levels, {
             0: 'bad',
            50: 'okay',
            80: 'good',
        })


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
        self.question.select_answer(self.answer3.hash)
        self.assertEquals(self.question.answered, True)


class RatingTestCase(TestCase):

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
