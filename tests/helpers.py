from unittest import TestCase

from elcuestionario.evaluation import Evaluator
from elcuestionario.loader import load


class AbstractTestCase(TestCase):

    def setUp(self):
        json_str = self._get_data_string()
        self.questionnaire, self.rating_levels = load(json_str)
        self.questions = self.questionnaire.get_questions()
        self.evaluator = Evaluator(self.rating_levels)
