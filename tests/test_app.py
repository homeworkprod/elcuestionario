# -*- coding: utf-8 -*-

try:
    unicode
except NameError:
    unicode = str  # Python 3

from nose2.tools import params

from elcuestionario import _create_app

from .helpers import AbstractTestCase


class AbstractFlaskTestCase(AbstractTestCase):

    def setUp(self):
        super(AbstractFlaskTestCase, self).setUp()

        app = _create_app(self.questionnaire, self.evaluator)
        self.client = app.test_client()
        self.form_data = {}

    def get(self):
        return self.client.get('/', data=self.form_data)

    def post(self):
        return self.client.post('/', data=self.form_data)

    def answer_question(self, question_text, answer_text):
        def find_by_text(items, text):
            for item in items:
                if item.text == text:
                    return item

        def find_question():
            return find_by_text(self.questions, question_text)

        def find_answer(question):
            answers = self.questionnaire.get_answers_for_question(question)
            return find_by_text(answers, answer_text)

        question = find_question()
        answer = find_answer(question)
        self._answer_question(question, answer)

    def answer_all_questions(self):
        for question in self.questions:
            self.answer_question_with_first_answer(question)

    def answer_question_with_first_answer(self, question):
        answers = list(self.questionnaire.get_answers_for_question(question))
        self._answer_question(question, answers[0])

    def _answer_question(self, question, answer):
        self.form_data[question.hash] = answer.hash


class FlaskTestCase(AbstractFlaskTestCase):

    def setUp(self):
        super(FlaskTestCase, self).setUp()

    def _get_data_string(self):
        return u'''{
    "title": "some title",
    "questions": [
        {
            "text": "some question",
            "answers": [
                { "text": "good answer",     "weighting": 1.0 },
                { "text": "mediocre answer", "weighting": 0.5 },
                { "text": "bad answer",      "weighting": 0.0 }
            ]
        },
        {
            "text": "another question",
            "answers": [
                { "text": "awesome answer",  "weighting": 1.1 },
                { "text": "okay-ish answer", "weighting": 0.666 }
            ]
        }
    ]
}
'''

    def test_get(self):
        result = self.get()

        for index, question in enumerate(self.questions, start=1):
            expected = '{0}. {1}'.format(index, question.text)
            assertResultBodyContains(result, expected)

    @params(
        (0, 2, 2),
        (1, 1, 2),
    )
    def test_post_incomplete(self, answered, remaining, total):
        for question in self.questions[:answered]:
            self.answer_question_with_first_answer(question)

        result = self.post()

        expected1 = \
            'You have answered only <strong>{0} of {1}</strong> questions so far.' \
            .format(answered, total)
        assertResultBodyContains(result, expected1)

        expected2 = \
            'Please answer the remaining <strong>{0}</strong> question(s)' \
            .format(remaining)
        assertResultBodyContains(result, expected2)

    @params(
        ('', 'stranger'),
        ('John Doe', 'John Doe'),
    )
    def test_username(self, given_username, expected_username):
        self.form_data['username'] = given_username
        self.answer_all_questions()

        result = self.post()

        expected = 'Your score, <em>{0}</em>'.format(expected_username)
        assertResultBodyContains(result, expected)

    @params(
        (
            [
                ('some question', 'bad answer'),
                ('another question', 'okay-ish answer'),
            ],
            '33.3'
        ),
        (
            [
                ('some question', 'good answer'),
                ('another question', 'awesome answer'),
            ],
            '105.0'
        ),
    )
    def test_score(self, questions_and_answers, expected_score):
        for question_text, answer_text in questions_and_answers:
            self.answer_question(question_text, answer_text)

        result = self.post()

        expected = '<p class="score">{0}&thinsp;%</p>'.format(expected_score)
        assertResultBodyContains(result, expected)


def assertResultBodyContains(result, expected):
    assert expected in unicode(result.data)
