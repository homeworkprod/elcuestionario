El Cuestionario
===============

**El Cuestionario** (formerly known as **Rate Yourself**) is a tiny web
application to display and evaluate single-page questionnaires.

A questionnaire (questions, their answers, and score ratings) is
defined as JSON_ in a single file.

The questions are presented in the order they are defined in the data
file while the answers are shown in random order.

Once all questions are answered, the user's score is calculated based
on the answers' weight (as defined) and is presented with a suitable
comment.

:Copyright: 2005-2015 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:Date: 02-Oct-2015 (original release: 26-Apr-2006)
:License: GNU General Public License version 2, see LICENSE for details.
:Version: 0.4.1


Requirements
------------

- Python_ 2.7+ or 3.3+
- Flask_


Installation
------------

Install dependencies:

.. code:: sh

    $ pip install -r requirements.txt

Make the script to run the application executable:

.. code:: sh

    $ chmod +x runserver.py

This script (which uses the built-in web server) is fine to get up and
running quickly. However, to actually serve the application on the
Internet, please consider the other `deployment options`_ described in
Flask's excellent documentation.


Configuration
-------------

Take a look at ``data/example.json`` regarding how a questionnaire is
defined. Just copy the file, adjust its content and update the value of
the ``SURVEY_FILENAME`` variable in the main script accordingly.


Title
+++++

A questionnaire has a title:

.. code:: json

    "title": "A Bunch of Questions",


Questions and Answers
+++++++++++++++++++++

Each question should have multiple answers.

Each answer must have weighting, defined as a float number between
``0.0`` and ``1.0``.

Exception: I sometimes use a value of ``1.1`` for "bonus answers" which
allows for an overall score of more than 100%.

To calculate the overall score, the weighting of each question's answer
will be used.

Example:

.. code:: json

    "questions": [
        {
            "text": "What's your favorite color?",
            "answers": [
                { "text": "blue",      "weighting": 0.7  },
                { "text": "green",     "weighting": 0.5  },
                { "text": "yellow",    "weighting": 0.1  },
                { "text": "red",       "weighting": 0.25 },
                { "text": "none",      "weighting": 1.0  },
                { "text": "checkered", "weighting": 1.1  }
            ]
        }
    ]


Ratings
+++++++

Ratings can be defined to add a text to the result based on the
achieved overall score. Each is bound to a score range.

The `minimum_score` value sets the threshold for each rating. The
adequate rating will be chosen by finding the one with the highest
`minimum_score` value that is lower than the score. For example, with a
score of 53 % and ratings with `minimum_score` values of
`[10, 20, ..., 90, 100]`, the selected rating will be the one with a
`minimum_score` value of ``50`` since it is lower than ``53`` and the
next higher `minimum_score` value, ``60``, is not lower than the score
of ``53``.

Therefore, a rating's `minimum_score` value defines the minimum score
one has to gain to be given that rating, as long as no other rating is
more suitable considering its `minimum_score` minimum.

Example:

.. code:: json

    "rating_levels": [
        { "minimum_score":  0, "text": "OMG, please waste time with something else!" },
        { "minimum_score": 40, "text": "Not bad." },
        { "minimum_score": 70, "text": "Looking good." },
        { "minimum_score": 90, "text": "Yeah, great result!" }
    ]

Rating levels are optional. If none are defined in the data file, to
rating text is shown on the result page.


Usage
-----

Start the application with the example configuration:

.. code:: sh

    $ ./runserver.py data/example.json

It will spawn a web server on port 5000.

To access the questionnaire, point a web browser to
http://localhost:5000/.

You can also specify a custom port to listen on as well as enable debug
mode:

.. code:: sh

    $ ./runserver.py --debug --port 8080 data/example.json


This will make the questionnaire available on http://localhost:8080/ and
provide an in-browser debugger in case an exception is raised by the
application.


Changes
-------

Notable changes since the first release:

- The data format for a questionnaire changed from XML to JSON_.

- WSGI_ (via Werkzeug_) has replaced CGI as the interface to the web
  server to support more `deployment options`_.

- Jinja_ has replaced Kid_ as the template engine.

- The original script evolved into a Flask_ application with separate
  modules and templates.

- Tests have been added.

- Naming has been adjusted to follow `PEP 8`_ more closely.

- Python 3 is supported.


.. _JSON:               http://www.json.com/
.. _Python:             http://www.python.org/
.. _Flask:              http://flask.pocoo.org/
.. _deployment options: http://flask.pocoo.org/docs/deploying/#deployment
.. _WSGI:               http://www.wsgi.org/
.. _Werkzeug:           http://werkzeug.pocoo.org/
.. _Jinja:              http://jinja.pocoo.org/
.. _Kid:                http://www.kid-templating.org/
.. _ElementTree:        http://effbot.org/zone/element-index.htm
.. _PEP 8:              http://www.python.org/dev/peps/pep-0008/
