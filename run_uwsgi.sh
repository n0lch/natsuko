#!/bin/bash
##  TODO: understand how threads, async, ugreen/greenlets work here
uwsgi -s /tmp/uwsgi.sock -C -w app:app --threads 4
