Rate Yourself
=============

**Rate Yourself** is a web-based framework for building surveys like
*How cool/geeky/whatever are you?*.

All survey-specific data (questions, their answers and score ratings)
is read from a single file containing XML data.

The questions and answers are presented to the user in random order.

When all questions are answered, the user's score is calculated based
on the answers' weight (as specified in the data file) and presented
with a suitable comment.


Requirements
------------

- Python_ 2.5+ (tested with 2.7.3)
- `Jinja 2`_ (tested with 2.7.1)


Installation
------------

- Make sure the required software is installed.

- *Note:* `Jinja 2`_ is a pure-Python package and thus can be installed
  (especially on webspace-only hostings) by simply uploading it.

- Make the package available to your script. If it is not already in
  your ``PYTHONPATH``, set the path in the imports section of the main
  script.

- The main script has to be executable:

  .. code:: sh

     $ chmod +x index.py

- Take a look at ``data/example.xml`` regarding how a survey is
  defined. Just copy the file, adjust its content and update the
  ``FILE_SURVEY`` variable in the main script accordingly.


.. _Python: http://www.python.org/
.. _Jinja 2: http://jinja.pocoo.org/


:Copyright: 2005-2013 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:Date: 04-Sep-2013 (original release: 26-Apr-2006)
:License: GNU General Public License version 2, see LICENSE for details.
