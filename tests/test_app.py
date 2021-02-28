"""
:Copyright: 2005-2021 Jochen Kupperschmidt
:License: GNU General Public License version 2, see LICENSE for details.
"""

import pytest

from elcuestionario.app import _create_app
from elcuestionario.evaluation import Evaluator
from elcuestionario.loader import load


@pytest.fixture(scope='module')
def questionnaire_and_rating_levels():
    data = '''{
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
    questionnaire, rating_levels = load(data)
    return questionnaire, rating_levels


@pytest.fixture(scope='module')
def questionnaire(questionnaire_and_rating_levels):
    return questionnaire_and_rating_levels[0]


@pytest.fixture(scope='module')
def questions(questionnaire):
    return questionnaire.get_questions()


@pytest.fixture(scope='module')
def evaluator(questionnaire_and_rating_levels):
    rating_levels = questionnaire_and_rating_levels[1]
    return Evaluator(rating_levels)


@pytest.fixture(scope='module')
def client(questionnaire, evaluator):
    app = _create_app(questionnaire, evaluator)
    return app.test_client()


def test_get(questions, client):
    result = client.get('/')

    for index, question in enumerate(questions, start=1):
        expected = f'{index}. {question.text}'
        assert_result_body_contains(result, expected)


@pytest.mark.parametrize(
    'answered, remaining, total',
    [
        (0, 2, 2),
        (1, 1, 2),
    ],
)
def test_post_incomplete(
    questionnaire, questions, client, answered, remaining, total
):
    form_data = {}

    for question in questions[:answered]:
        answer_question_with_first_answer(questionnaire, question, form_data)

    result = submit_form(client, form_data)

    expected1 = f'You have answered only <strong>{answered} of {total}</strong> questions so far.'
    assert_result_body_contains(result, expected1)

    expected2 = (
        f'Please answer the remaining <strong>{remaining}</strong> question(s)'
    )
    assert_result_body_contains(result, expected2)


@pytest.mark.parametrize(
    'given_username, expected_username',
    [
        ('', 'stranger'),
        ('John Doe', 'John Doe'),
    ],
)
def test_username(
    questionnaire, questions, client, given_username, expected_username
):
    form_data = {'username': given_username}

    for question in questions:
        answer_question_with_first_answer(questionnaire, question, form_data)

    result = submit_form(client, form_data)

    expected = f'Your score, <em>{expected_username}</em>'
    assert_result_body_contains(result, expected)


@pytest.mark.parametrize(
    'questions_and_answers, expected_score',
    [
        (
            [
                ('some question', 'bad answer'),
                ('another question', 'okay-ish answer'),
            ],
            '33.3',
        ),
        (
            [
                ('some question', 'good answer'),
                ('another question', 'awesome answer'),
            ],
            '105.0',
        ),
    ],
)
def test_score(
    client, questionnaire, questions, questions_and_answers, expected_score
):
    form_data = {}

    for question_text, answer_text in questions_and_answers:
        answer_question(
            questionnaire, questions, question_text, answer_text, form_data
        )

    result = submit_form(client, form_data)

    expected = f'<p class="score">{expected_score}&thinsp;%</p>'
    assert_result_body_contains(result, expected)


def answer_question(
    questionnaire, questions, question_text, answer_text, form_data
):
    question = find_by_text(questions, question_text)

    answers = questionnaire.get_answers_for_question(question)
    answer = find_by_text(answers, answer_text)

    form_data[question.hash] = answer.hash


def find_by_text(items, text):
    for item in items:
        if item.text == text:
            return item


def answer_question_with_first_answer(questionnaire, question, form_data):
    answers = list(questionnaire.get_answers_for_question(question))
    form_data[question.hash] = answers[0].hash


def submit_form(client, form_data):
    return client.post('/', data=form_data)


def assert_result_body_contains(result, expected):
    assert expected in result.get_data(as_text=True)
