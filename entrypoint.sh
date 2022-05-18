#!/usr/bin/env bash
./manage.py migrate
uwsgi --ini uwsgi.ini
