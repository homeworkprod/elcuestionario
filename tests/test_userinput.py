"""
:Copyright: 2005-2021 Jochen Kupperschmidt
:License: GNU General Public License version 2, see LICENSE for details.
"""

from elcuestionario.loader import load
from elcuestionario.userinput import UserInput


def test_answered():
    data = '''{
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

    questionnaire, rating_levels = load(data)
    questions = questionnaire.get_questions()

    question = questions[0]

    answer1, answer2, answer3 = questionnaire.get_answers_for_question(question)

    user_input = UserInput([question.hash])

    def is_answer_selected(answer):
        return user_input.is_answer_selected(question, answer)

    assert is_answer_selected(answer1) == False
    assert is_answer_selected(answer2) == False
    assert is_answer_selected(answer3) == False

    user_input.answer_question(question.hash, answer2.hash)

    assert is_answer_selected(answer1) == False
    assert is_answer_selected(answer2) == True
    assert is_answer_selected(answer3) == False
