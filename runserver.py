#!/usr/bin/env python

from elcuestionario import create_app


app = create_app('data/example.json')
app.run(port=5000, debug=False)
