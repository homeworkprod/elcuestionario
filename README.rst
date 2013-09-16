El Cuestionario
===============

**El Cuestionario** (formerly known as **Rate Yourself**) is a tiny web
application to display and evaluate single-page questionnaires.

A questionnaire (questions, their answers, and score ratings) is
defined as XML in a single file.

The questions are presented in the order they are defined in the
definition while the answers are shown in random order.

Once all questions are answered, the user's score is calculated based
on the answers' weight (as defined) and is presented with a suitable
comment.


Requirements
------------

- Python_ 2.6+ or 3.3+
- Flask_ (tested with 0.10.1)


Installation
------------

Install Flask_:

.. code:: sh

   $ pip install Flask

Make the script to run the application executable:

.. code:: sh

   $ chmod +x runserver.py

This script (which uses the built-in web server) is fine to get up and
running quickly. However, to actually serve the application on the
Internet, please consider the other `deployment options`_ described in
Flask's excellent documentation.


Configuration
-------------

Take a look at ``data/example.xml`` regarding how a questionnaire is
defined. Just copy the file, adjust its content and update the value of
the ``SURVEY_FILENAME`` variable in the main script accordingly.


Title
+++++

A questionnaire has a title. Set it as text value of the ``title`` element:

.. code:: xml

    <title>A Bunch of Questions</title>


Questions and Answers
+++++++++++++++++++++

Each question should have multiple answers.

Each answer must have weighting, defined as a float number between
``0.0`` and ``1.0``.

Exception: I sometimes use a value of ``1.1`` for "bonus answers" which
allows for an overall score of more than 100%).

To calculate the overall score, the weighting of each question's answer
will be used.

Example:

.. code:: xml

    <questions>
        <question title="What's your favorite color?">
            <answer title="blue" weighting="0.7"/>
            <answer title="green" weighting="0.5"/>
            <answer title="yellow" weighting="0.1"/>
            <answer title="red" weighting="0.25"/>
            <answer title="none" weighting="1.0"/>
            <answer title="checkered" weighting="1.1"/>
        </question>
    </questions>


Ratings
+++++++

Ratings can be defined to add a text to the result based on the
achieved overall score. Each is bound to a score range.

The `minscore` value sets the threshold for each rating. The adequate
rating will be chosen by finding the one with the highest `minscore`
value that is lower than the score. For example, with a score of 53 %
and ratings with `minscore` values of `[10, 20, ..., 90, 100]`, the
selected rating will be the one with a `minscore` value of ``50`` since
it is lower than ``53`` and the next higher `minscore` value, ``60``,
is not lower than the score of ``53``.

Therefore, a rating's `minscore` value defines the minimum score one
has to gain to be given that rating, as long as no other rating is more
suitable considering its `minscore` minimum.

Example:

.. code:: xml

    <ratings>
        <rating minscore="0">OMG, please waste time with something else!</rating>
        <rating minscore="40">Not bad.</rating>
        <rating minscore="70">Looking good.</rating>
        <rating minscore="90">Yeah, great result!</rating>
    </ratings>


Usage
-----

Start the application:

.. code:: sh

   $ ./runserver.py

It will spawn a web server on port 5000.

To access the questionnaire, point a web browser to
http://localhost:5000.


Changes
-------

Notable changes since the first release:

- WSGI_ (via Werkzeug_) has replaced CGI as the interface to the web
  server to support more `deployment options`_.

- Jinja_ has replaced Kid_ as the template engine.

- The original script evolved into a Flask application with separate
  modules and templates.

- Tests have been added.

- ElementTree is imported from the standard library (which includes it
  as of Python 2.5).

- Naming has been adjusted to follow `PEP 8`_ more closely.


.. _Python:             http://www.python.org/
.. _Flask:              http://flask.pocoo.org/
.. _deployment options: http://flask.pocoo.org/docs/deploying/#deployment
.. _WSGI:               http://www.wsgi.org/
.. _Werkzeug:           http://werkzeug.pocoo.org/
.. _Jinja:              http://jinja.pocoo.org/
.. _Kid:                http://www.kid-templating.org/
.. _ElementTree:        http://effbot.org/zone/element-index.htm
.. _PEP 8:              http://www.python.org/dev/peps/pep-0008/


:Copyright: 2005-2013 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:Date: 11-Sep-2013 (original release: 26-Apr-2006)
:License: GNU General Public License version 2, see LICENSE for details.
