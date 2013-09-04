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
import random
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
    l = self.values()
    random.shuffle(l)
    return l

# ---------------------------------------------------------------- #

class Survey(object):
    """A set of questions, answers, selection states and rating levels."""

    def __init__(self, file=None):
        self.title = u'Untitled'
        self.questions = QuestionPool()
        self.rating_levels = {}

        # Read XML data from file.
        if file is not None:
            etree = ET.parse(file)

            # title
            self.title = etree.find('title').text

            # questions and their answers
            for qe in etree.getiterator('question'):
                q = Question(qe.get('caption'))
                for ae in qe.getiterator('answer'):
                    a = Answer(ae.get('caption'), float(ae.get('weighting')))
                    q[a.hash] = a
                self.questions[q.hash] = q

            # ratings
            for re in etree.getiterator('rating'):
                self.rating_levels[int(re.get('minscore'))] = re.text

    def __str__(self):
        return '<%s, %d questions, %d rating levels>' \
            % (self.__class__.__name__, len(self.questions),
                len(self.rating_levels))

    def calculate_score(self):
        """Calculate the score depending on the given answers."""
        assert self.questions.all_answered()
        score = 0
        for q in self.questions.values():
            score += q.selected_answer().weighting
        return int(float(score) / len(self.questions) * 100)

    def get_rating(self, score):
        """Return the rating text for the given score."""
        minscores = self.rating_levels.keys()
        minscores.sort()
        minscores.reverse()
        for minscore in minscores:
            if score >= minscore:
                return self.rating_levels[minscore]

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

    def number_answered(self):
        """Return the number of questions that have already been answered."""
        n = 0
        for q in self.values():
            if q.answered:
                n += 1
        return n

    def number_unanswered(self):
        """Return the number of questions that have not been answered yet."""
        return len(self) - self.number_answered()

    def all_answered(self):
        """Tell if all questions in the pool were answered."""
        for q in self.values():
            if not q.answered:
                return False
        return True

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

    def answer(self, answer_hash):
        """Answer the question by choosing an answer."""
        self[answer_hash].selected = True
        self.answered = True

    def selected_answer(self):
        """Return the chosen answer."""
        for a in self.values():
            if a.selected:
                return a

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
    survey = Survey(FILE_SURVEY)

    output = {
        'title': survey.title,
        'questions': survey.questions,
        'submitted': False,
    }

    return render_template('questionnaire.html', **output)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    survey = Survey(FILE_SURVEY)
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
