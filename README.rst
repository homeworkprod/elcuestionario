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

- Python_ 2.3 (tested with 2.3.5)
- ElementTree_ (tested with 1.2.6)
- Kid_ (tested with 0.9.1)


Installation
------------

- Make sure the required software is installed.

- *Note:* ElementTree_ and Kid_ are pure-Python packages and can be
  installed (especially on webspace-only hostings) by simply uploading
  them.

- Make those packages available to your script. If they are not already
  in your ``PYTHONPATH``, set the path in the imports section of the
  main script.

- The main script has to be executable:

  .. code:: sh

     $ chmod +x index.py

- Take a look at ``data/example.xml`` regarding how a survey is
  defined. Just copy the file, adjust its content and update the
  ``FILE_SURVEY`` variable in the main script accordingly.


.. _Python: http://www.python.org/
.. _ElementTree: http://effbot.org/zone/element-index.htm
.. _Kid: http://kid.lesscode.org/


:Copyright: 2005-2013 `Jochen Kupperschmidt <http://homework.nwsnet.de/>`_
:Date: 08-May-2006 (original release: 26-Apr-2006)
:License: GNU General Public License version2, see LICENSE for details.
