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

- Python_ 2.5+ (tested with 2.7.3)
- Flask_ (tested with 0.10.1)


Installation
------------

- Make sure the required software is installed.

- Make additionally installed packages available to your script. If
  they are not already in your ``PYTHONPATH``, set the path in the
  imports section of the main script.

- The main script has to be executable:

  .. code:: sh

     $ chmod +x elcuestionario.py


Configuration
-------------

Take a look at ``data/example.xml`` regarding how a questionnaire is
defined. Just copy the file, adjust its content and update the value of
the ``FILE_SURVEY`` variable in the main script accordingly.


Usage
-----

Start the application on the command line:

.. code:: sh

   $ ./elcuestionario.py

It will spawn a web server on port 5000.

Access the questionnaire by pointing your web browser to
``http://localhost:5000``.


.. _Python:   http://www.python.org/
.. _Flask:    http://flask.pocoo.org/


:Copyright: 2005-2013 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:Date: 10-Sep-2013 (original release: 26-Apr-2006)
:License: GNU General Public License version 2, see LICENSE for details.
