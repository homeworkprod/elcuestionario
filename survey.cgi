#!/usr/bin/env python

from wsgiref.handlers import CGIHandler

from survey import app

CGIHandler().run(app)
