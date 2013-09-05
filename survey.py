#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

from collections import namedtuple
from random import shuffle
import sha
import sys
import xml.etree.ElementTree as ET

# If it isn't already in your path, add Jinja with this line.
#sys.path.append('/path/to/your/site-packages')

from flask import Flask, render_template, request


# configuration
FILE_SURVEY = 'data/example.xml'


app = Flask(__name__)

# ---------------------------------------------------------------- #

class ObjectWithHash(object):
    """A hash value will be stored when the caption is set."""

    def __init__(self, caption):
        self.caption = caption

    def _get_caption(self):
        return self.__caption

    def _set_caption(self, value):
        self.__caption = unicode(value)
        self.hash = sha.new(
            self.__caption.encode('latin-1')).hexdigest()[:8]

    caption = property(_get_caption, _set_caption)


def randomized_values(self):
    """Return a randomized list of values."""
    values = self.values()
    shuffle(values)
    return values

# ---------------------------------------------------------------- #

class ParsedSurveyData(object):

    def __init__(self, filename):
        self.tree = ET.parse(filename)

    def get_survey(self):
        survey = Survey(self.get_title())
        questions = map(self.get_question, self.tree.getiterator('question'))
        for question in questions:
            survey.add_question(question)
        for min_score, text in self.get_rating_levels():
            survey.add_rating_level(min_score, text)
        return survey

    def get_title(self):
        return self.tree.find('title').text

    def get_question(self, element):
        caption = element.get('caption')
        question = Question(caption)
        answers = map(self.get_answer, element.getiterator('answer'))
        for answer in answers:
            question.add_answer(answer)
        return question

    def get_answer(self, element):
        caption = element.get('caption')
        weighting = float(element.get('weighting'))
        return Answer(caption, weighting)

    def get_rating_levels(self):
        for element in self.tree.getiterator('rating'):
            min_score = int(element.get('minscore'))
            yield min_score, element.text


class Survey(object):
    """A set of questions, answers, selection states and rating levels."""

    def __init__(self, title):
        self.title = title
        self.questions = QuestionPool()
        self.rating_levels = {}

    @classmethod
    def from_file(cls, filename):
        """Create a survey from XML data read from a file."""
        return ParsedSurveyData(filename).get_survey()

    def __str__(self):
        return '<%s, %d questions, %d rating levels>' \
            % (self.__class__.__name__, len(self.questions),
                len(self.rating_levels))

    def add_question(self, question):
        self.questions[question.hash] = question

    def add_rating_level(self, min_score, text):
        self.rating_levels[min_score] = text

    def calculate_score(self):
        """Calculate the score depending on the given answers."""
        assert self.questions.all_answered()
        score = sum(question.selected_answer().weighting
            for question in self.questions.values())
        return float(score) / len(self.questions) * 100

    def get_rating(self, score):
        """Return the rating text for the given score."""
        min_scores = self.rating_levels.keys()
        min_scores.sort()
        min_scores.reverse()
        for min_score in min_scores:
            if score >= min_score:
                return self.rating_levels[min_score]

    def get_result(self):
        """Return the evaluation result."""
        score = self.calculate_score()
        rating = self.get_rating(score)
        return Result(score, rating)


Result = namedtuple('Result', 'score rating')

# ---------------------------------------------------------------- #

class QuestionPool(dict):
    """A pool of questions."""

    get_questions = randomized_values

    def total_answered(self):
        """Return the number of questions that have already been answered."""
        return sum(1 for question in self.values() if question.answered)

    def total_unanswered(self):
        """Return the number of questions that have not been answered yet."""
        return len(self) - self.total_answered()

    def all_answered(self):
        """Tell if all questions in the pool were answered."""
        return all(question.answered for question in self.values())

# ---------------------------------------------------------------- #

class Question(dict, ObjectWithHash):
    """A question with multiple answers."""

    def __init__(self, caption):
        ObjectWithHash.__init__(self, caption)
        self.answered = False

    def __str__(self):
        return '<%s, hash=%s, caption="%s", %d answers, answered=%s>' \
            % (self.__class__.__name__, self.hash,
                self.caption.encode('latin-1'),
                len(self), self.answered)

    def add_answer(self, answer):
        self[answer.hash] = answer

    def answer(self, answer_hash):
        """Answer the question by choosing an answer."""
        self[answer_hash].selected = True
        self.answered = True

    def selected_answer(self):
        """Return the chosen answer."""
        return next(answer for answer in self.values() if answer.selected)

    get_answers = randomized_values

# ---------------------------------------------------------------- #

class Answer(ObjectWithHash):
    """An answer to a question."""

    def __init__(self, caption, weighting):
        ObjectWithHash.__init__(self, caption)
        self.weighting = weighting
        self.selected = False

    def __str__(self):
        return '<%s, hash=%s, caption="%s", weighting=%f, selected=%s>' \
            % (self.__class__.__name__, self.hash,
                self.caption.encode('latin-1'),
                self.weighting, self.selected)

# ---------------------------------------------------------------- #

@app.route('/')
def view():
    survey = Survey.from_file(FILE_SURVEY)

    output = {
        'title': survey.title,
        'questions': survey.questions,
        'submitted': False,
    }

    return render_template('questionnaire.html', **output)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    survey = Survey.from_file(FILE_SURVEY)
    username = request.form['username']

    output = {
        'title': survey.title,
        'username': username,
    }

    # Examine which questions were answered and which answer was selected.
    for name, value in request.form.items():
        if name.startswith('q_') and value.startswith('a_'):
            survey.questions[name[2:]].answer(value[2:])

    if survey.questions.all_answered():
        output['result'] = survey.get_result()
        return render_template('result.html', **output)
    else:
        output['questions'] = survey.questions
        output['submitted'] = True
        return render_template('questionnaire.html', **output)

# ---------------------------------------------------------------- #

if __name__ == '__main__':
    app.run(port=8080, debug=False)
