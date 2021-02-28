"""
:Copyright: 2005-2021 Jochen Kupperschmidt
:License: GNU General Public License version 2, see LICENSE for details.
"""

from elcuestionario.evaluation import RatingLevel
from elcuestionario.loader import load


def test_load():
    data = '''{
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

    questionnaire, rating_levels = load(data)
    questions = questionnaire.get_questions()

    assert questionnaire.title == 'The Title'

    assert len(questions) == 2

    question1 = questions[0]
    assert question1.text == 'question 1'
    assert_answer_texts(
        questionnaire,
        question1,
        {
            'answer 1.1',
            'answer 1.2',
            'answer 1.3',
        },
    )

    question2 = questions[1]
    assert question2.text == 'question 2'
    assert_answer_texts(
        questionnaire,
        question2,
        {
            'answer 2.1',
            'answer 2.2',
            'answer 2.3',
            'answer 2.4',
            'answer 2.5',
        },
    )

    assert rating_levels == [
        RatingLevel( 0, 'bad'),
        RatingLevel(50, 'okay'),
        RatingLevel(80, 'good'),
    ]


def test_load_unicode():
    data = '''{
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

    questionnaire, rating_levels = load(data)
    questions = questionnaire.get_questions()

    assert questionnaire.title == 'Frägebögen'

    assert len(questions) == 1

    question = questions[0]
    assert question.text == 'Farbtöne'
    assert_answer_texts(
        questionnaire,
        question,
        {
            'weiß',
            'grün',
            'rötlich',
        },
    )

    assert rating_levels == [
        RatingLevel(0, 'großartig'),
    ]


def assert_answer_texts(questionnaire, question, expected):
    answers = questionnaire.get_answers_for_question(question)
    texts = {answer.text for answer in answers}
    assert texts == expected
