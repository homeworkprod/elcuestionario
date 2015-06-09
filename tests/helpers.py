# -*- coding: utf-8 -*-

from io import StringIO
from unittest import TestCase

from elcuestionario.evaluation import Evaluator
from elcuestionario.loader import load


class AbstractTestCase(TestCase):

    def setUp(self):
        self.questionnaire, self.rating_levels = self._load_data()
        self.questions = self.questionnaire.get_questions()
        self.evaluator = Evaluator(self.rating_levels)

    def _load_data(self):
        data = self._get_data_string()
        f = StringIO(data)
        return load(f)
