# Fridge2Table
A simple recipe recommender :)
## Installation
### Project Setup
1. Clone the Repository
2. Install Python3
3. Go to Project Folder and run virtual env: `virtualenv .venv`, `source .venv/bin/activate`
4. Install Django in virtual env: `pip install --upgrade pip`, `pip install django`
5. Install requirements: `pip install -r requirements.txt`
6. Follow the Database Setup Instruction
7. To create migrations: `python manage.py makemigrations`, `python manage.py migrate`
8. To make static files load, run : `python manage.py collectstatic`
9. To run the application: `python manage.py runserver`
### Postgresql Database Setup
1. Install Postgresql and setup your postgres user.
2. Run application pgAdmin
3. Create a Database : `fridge-2-table` under Databases
4. Enter all the DB Details in the `.env` file or `settings.py` file
5. If migrations give error, trying changing password in the .env file to the one that you set when you started the pgAdmin application.
### Core
1. Place you csvs in `main/core/csv`
2. Modify scripts in `main/core`
3. Code work done in `main/core/work`
### Deployment
1. Create a DO account and make a droplet
2. Install the repository as usual
3. Configure nginx and gunicorn to serve
### Logging
1. To enable logging, uncomment the Logging code in env file and set DEBUG = True
2. To use logger to log details, add this lines to the top of your file:<br />
    `import logging`<br />
    `logger = logging.getLogger(__name__)`
3. To use it, write `logger.debug('Add what you want to print')`