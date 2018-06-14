# BM systems
This is a web-app that can be used to generate and analyse data from social networks about brands, products, customers etc.

## Setup proccess
1) Setup virtualenv
2) Install dependened libraries with pip install -r requirements.txt
3) Create database, psql user-password and set it in DB portion of Brands/settings.py 
4) Run 'makemigrations' and 'migrate' to configure PSQL DB to project's models
5) Create admin account with 'createsuperuser'
6) Run 'runserver' to start project on localhost
7) Run celery in separate terminal under virtualenv - "celery worker -A Brands --loglevel=debug --concurrency=4"

## Requirements
1) Python 3
2) Django
3) PostgreSQL
4) Redis