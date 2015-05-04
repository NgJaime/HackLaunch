#!/usr/bin/env bash

coverage run manage.py test -v 2
coverage html
