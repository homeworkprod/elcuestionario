"""
:Copyright: 2005-2021 Jochen Kupperschmidt
:License: GNU General Public License version 2, see LICENSE for details.
"""

import pytest

from elcuestionario.evaluation import Evaluator, RatingLevel
from elcuestionario.loader import load


@pytest.mark.parametrize(
    'score, expected',
    [
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
    ],
)
def test_rating(score, expected):
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

    evaluator = Evaluator(rating_levels)

    assert evaluator.get_rating_text(score) == expected


def test_without_rating_texts():
    data = '''{
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
    _, rating_levels = load(data)

    evaluator = Evaluator(rating_levels)
    score = 0.5

    assert evaluator.get_rating_text(score) is None
