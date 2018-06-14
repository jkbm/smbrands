# smbrands

## Setup proccess
1) Setup virtualenv
2) Install dependened libraries with pip install -r requirements.txt
3) Create database, psql user-password and set it in DB portion of Brands/settings.py 
4) Run 'makemigrations' and 'migrate' to configure PSQL DB to project's models
5) Create admin account with 'createsuperuser'
6) Run 'runserver' to start project on localhost