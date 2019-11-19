#!/usr/bin/env bash
python3 manage.py makemigrations
python3 manage.py migrate
systemctl restart apache2