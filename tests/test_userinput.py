# -*- coding: utf-8 -*-

from elcuestionario.userinput import UserInput

from .helpers import AbstractTestCase


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

        self.answer1, self.answer2, self.answer3 = \
            self.questionnaire.get_answers_for_question(self.question)

        self.user_input = UserInput([self.question.hash])

    def test_answered(self):
        self.assertAnswerIsSelected(self.answer1, False)
        self.assertAnswerIsSelected(self.answer2, False)
        self.assertAnswerIsSelected(self.answer3, False)

        self.user_input.answer_question(self.question.hash, self.answer2.hash)

        self.assertAnswerIsSelected(self.answer1, False)
        self.assertAnswerIsSelected(self.answer2, True)
        self.assertAnswerIsSelected(self.answer3, False)

    def assertAnswerIsSelected(self, answer, expected):
        actual = self.user_input.is_answer_selected(self.question, answer)
        self.assertEqual(actual, expected)
