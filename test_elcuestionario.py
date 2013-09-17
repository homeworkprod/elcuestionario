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

from io import StringIO
from unittest import TestCase

from nose2.tools import params

from elcuestionario.loader import load_questionnaire
from elcuestionario.models import Evaluator, RatingLevel, UserInput


class AbstractTestCase(TestCase):

    def setUp(self):
        self.questionnaire = self._load_questionnaire()

    def _load_questionnaire(self):
        data = self._get_data_string()
        f = StringIO(data)
        return load_questionnaire(f)


class AbstractLoaderTestCase(AbstractTestCase):

    def setUp(self):
        super(AbstractLoaderTestCase, self).setUp()

        self.title = self.questionnaire.title
        self.questions = self.questionnaire.get_questions()
        self.rating_levels = self.questionnaire.rating_levels

    def assertTitleEqual(self, expected):
        self.assertEqual(self.title, expected)

    def assertAnswersEqual(self, question_index, expected):
        answers = self._get_answers(question_index)
        texts = self._get_answer_texts(answers)
        self.assertEqual(texts, expected)

    def _get_answers(self, question_index):
        question = self.questions[question_index]
        return self.questionnaire.get_answers_for_question(question)

    def _get_answer_texts(self, answers):
        return set(answer.text for answer in answers)


class LoaderTestCase(AbstractLoaderTestCase):

    def _get_data_string(self):
        return u'''{
    "title": "The Title",
    "questions": [
        {
            "text": "question 1",
            "answers": [
                { "text": "answer 1.1", "weighting": 0.0 },
                { "text": "answer 1.2", "weighting": 0.5 },
                { "text": "answer 1.3", "weighting": 1.0 }
            ]
        },
        {
            "text": "question 2",
            "answers": [
                { "text": "answer 2.1", "weighting": 0.0  },
                { "text": "answer 2.2", "weighting": 0.25 },
                { "text": "answer 2.3", "weighting": 0.5  },
                { "text": "answer 2.4", "weighting": 0.75 },
                { "text": "answer 2.5", "weighting": 1.0  }
            ]
        }
    ],
    "rating_levels": [
        { "minimum_score":  0, "text": "bad"  },
        { "minimum_score": 50, "text": "okay" },
        { "minimum_score": 80, "text": "good" }
    ]
}
'''

    def test_title(self):
        self.assertTitleEqual('The Title')

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
        return u'''{
    "title": "Frägebögen",
    "questions": [
        {
            "text": "Farbtöne",
            "answers": [
                { "text": "weiß",    "weighting": 1.0 },
                { "text": "grün",    "weighting": 1.0 },
                { "text": "rötlich", "weighting": 1.0 }
            ]
        }
    ],
    "rating_levels": [
        { "minimum_score": 0, "text": "großartig" }
    ]
}
'''

    def test_title(self):
        self.assertTitleEqual(u'Frägebögen')

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


class QuestionTestCase(AbstractTestCase):

    def _get_data_string(self):
        return u'''{
    "title": "some title",
    "questions": [
        {
            "text": "some question",
            "answers": [
                { "text": "yes",   "weighting": 1.0 },
                { "text": "maybe", "weighting": 0.5 },
                { "text": "no",    "weighting": 0.0 }
            ]
        }
    ],
    "rating_levels": []
}
'''

    def setUp(self):
        super(QuestionTestCase, self).setUp()

        self.question = self.questionnaire.get_questions()[0]

        answers = list(self.questionnaire.get_answers_for_question(self.question))
        self.answer1 = answers[0]
        self.answer2 = answers[1]
        self.answer3 = answers[2]

        self.user_input = UserInput([self.question.hash])

    def assertAnswerIsSelected(self, answer, expected):
        actual = self.user_input.is_answer_selected(self.question, answer)
        self.assertEquals(actual, expected)

    def test_answered(self):
        self.assertAnswerIsSelected(self.answer1, False)
        self.assertAnswerIsSelected(self.answer2, False)
        self.assertAnswerIsSelected(self.answer3, False)

        self.user_input.answer_question(self.question.hash, self.answer2.hash)

        self.assertAnswerIsSelected(self.answer1, False)
        self.assertAnswerIsSelected(self.answer2, True)
        self.assertAnswerIsSelected(self.answer3, False)


class RatingTestCase(TestCase):

    def setUp(self):
        rating_levels = [RatingLevel(minimum_score, text)
            for minimum_score, text in [
                (  0, 'worst'),
                ( 30, 'oh-oh'),
                ( 60, 'OK-ish'),
                ( 90, 'great'),
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
