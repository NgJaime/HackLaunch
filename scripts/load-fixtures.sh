#!/usr/bin/env bash

python manage.py loaddata users/fixtures/skills.json
python manage.py loaddata users/fixtures/maker_types.json
