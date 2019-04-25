# ictlife-mms

This application is hosted on <a href="https://heroku.com">Heroku</a> and can be accessed using the url: https://ictlife-mms.herokuapp.com/
The code for this application is available on <a href="https://github.com/rayalois22/ictlife-mms">Github</a>

In order to build and run it on a different envireonment, you will need the following:
    1. Python-3.x
    2. Postgresql database
        <code>sudo apt-get install postgresql postgresql-contrib</code>
    3. Python3-venv
        <kbd>sudo apt install python3-venv</kbd>
Once the above two requirements are met, then you can follow the following steps to set up 
a virtual environment and build the application.

1. Create a supperuser account for the Postgres database or use the default <em>postgres</em> user:
    <kbd>sudo -u postgres createuser --superuser name_of_user</kbd>
2. Assuming you chose to use the default <em>postgres</em> user, create a the database called <em>mms</em>
    <kbd>sudo -u postgres createdb mms</kbd>
3. Confirm that the database was created by logging into it:
    <kbd>sudo -u postgres psql -d mms</kbd>
4. Create the project directory
    <kbd>mkdir ~/Desktop/ictlife-mms && cd ~/Desktop/ictlife-mms</kbd>
5. Create project virtual environmentin the project directory
    <kbd>python3 -m venv env</kbd>
6. Activate the virtual environment
    <kbd>source env/bin/activate</kbd>
7. Install project dependencies as below
    <kbd>pip install flask</kbd>
    <kbd>pip install flask_sqlalchemy</kbd>
    <kbd>pip install psycopg2-binary</kbd>
    <kbd>pip install flask_script</kbd>
    <kbd>pip install flask_migrate</kbd>
8. At this point you can clone the project from Github or unzip the downloaded zip file in the project folder(ictlife-mms)
    <kbd>git clone https://github.com/rayalois22/ictlife-mms.git</kbd>
9. Run database migrations
    <kbd>python manage.py db upgrade</kbd>
10. Find <em>app.py</em> in the project root folder and make sure to uncomment the lines below if they are commented.
    <kbd>os.environ['DATABASE_URL'] = "postgresql:///mms"</kbd>
    <kbd>os.environ['APP_SETTINGS'] = "config.DevelopmentConfig"</kbd>
11. Run the application
    <kbd>flask run</kbd>
