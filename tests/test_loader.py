# -*- coding: utf-8 -*-

from elcuestionario.evaluation import RatingLevel

from .helpers import AbstractTestCase


class AbstractLoaderTestCase(AbstractTestCase):

    def setUp(self):
        super(AbstractLoaderTestCase, self).setUp()

        self.title = self.questionnaire.title

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
