#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2005-2013 Jochen Kupperschmidt
# Released under the terms of the GNU General Public License
#  _                               _
# | |_ ___ _____ ___ _ _ _ ___ ___| |_
# |   | . |     | ._| | | | . |  _| . /
# |_|_|___|_|_|_|___|_____|___|_| |_|_\
#   http://homework.nwsnet.de/

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


def randomizedValues(self):
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
        self.ratingLevels = {}

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
                self.ratingLevels[int(re.get('minscore'))] = re.text

    def __str__(self):
        return '<%s, %d questions, %d rating levels>' \
            % (self.__class__.__name__, len(self.questions),
                len(self.ratingLevels))

    def calculateScore(self):
        """Calculate the score depending on the given answers."""
        assert self.questions.allAnswered()
        score = 0
        for q in self.questions.values():
            score += q.selectedAnswer().weighting
        return int(float(score) / len(self.questions) * 100)

    def getRating(self, score):
        """Return the rating text for the given score."""
        minscores = self.ratingLevels.keys()
        minscores.sort()
        minscores.reverse()
        for minscore in minscores:
            if score >= minscore:
                return self.ratingLevels[minscore]

# ---------------------------------------------------------------- #

class QuestionPool(dict):
    """A pool of questions."""

    getQuestions = randomizedValues

    def numberAnswered(self):
        """Return the number of questions that have already been answered."""
        n = 0
        for q in self.values():
            if q.answered:
                n += 1
        return n

    def numberUnanswered(self):
        """Return the number of questions that have not been answered yet."""
        return len(self) - self.numberAnswered()

    def allAnswered(self):
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

    def answer(self, answerHash):
        """Answer the question by choosing an answer."""
        self[answerHash].selected = True
        self.answered = True

    def selectedAnswer(self):
        """Return the chosen answer."""
        for a in self.values():
            if a.selected:
                return a

    getAnswers = randomizedValues

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

class Result(object):
    """A user's survey result."""

    def __init__(self, **kwargs):
        for k, v in kwargs.iteritems():
            setattr(self, k, v)

# ---------------------------------------------------------------- #

@app.route('/')
def view():
    survey = Survey(FILE_SURVEY)

    output = {
        'submitted': False,
        'title': survey.title,
        'questions': survey.questions,
    }

    return render_template('questionnaire.html', **output)

@app.route('/evaluate', methods=['POST'])
def evaluate():
    survey = Survey(FILE_SURVEY)

    username = request.form['username']
    output = {
        'submitted': True,
        'username': username,
        'title': survey.title,
        'questions': survey.questions,
    }

    # Examine which questions were answered and which answer was selected.
    for name, value in request.form.items():
        if name.startswith('q_') and value.startswith('a_'):
            survey.questions[name[2:]].answer(value[2:])

    # Compile result.
    if survey.questions.allAnswered():
        score = survey.calculateScore()
        output['result'] = Result(
            username=username,
            score=score,
            rating=survey.getRating(score))
        return render_template('result.html', **output)
    else:
        return render_template('questionnaire.html', **output)

if __name__ == '__main__':
    app.run(port=8080, debug=False)
