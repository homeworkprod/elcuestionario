# -*- coding: utf-8 -*-

from io import StringIO
from unittest import TestCase

from elcuestionario.loader import load


class AbstractTestCase(TestCase):

    def setUp(self):
        self.questionnaire, self.evaluator = self._load_data()
        self.questions = self.questionnaire.get_questions()

    def _load_data(self):
        data = self._get_data_string()
        f = StringIO(data)
        return load(f)
