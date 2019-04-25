from flask import Flask, redirect, render_template, request, jsonify, session, flash, send_from_directory, url_for
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import csv
import os
import re
from datetime import datetime
# from validate_email import validate_email

# Sets the environment variables
os.environ['FLASK_APP'] = "app.py"

# UNCOMMENT 2 LINES BELOW ON LOCALHOST
# os.environ['DATABASE_URL'] = "postgresql:///mms"
# os.environ['APP_SETTINGS'] = "config.DevelopmentConfig"

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

now = datetime.now()
 
site = {
    'name': 'ICTLife MMS',
    'errors': [] 
}

from models import Category, Member, Contribution, ValidContribution

@app.route("/")
def index():
    valid_records = get_valid_contributions()
    if not valid_records:
        return render_template("index.html", now=now, site=site, records=[])
    return render_template('index.html', now=now, site=site, records=valid_records)

@app.route("/create/member", methods=['GET', 'POST'])
def create_member():
    if request.method == 'GET':
        categories = get_categories()
        return render_template("create_member.html", now=now, site=site, categories=categories)
    first_name = request.form.get('first_name')
    other_names = request.form.get('other_names')
    email = request.form.get('email')
    category = request.form.get('category')
    try:
        member = Member(first_name, other_names, email, category)
        db.session.add(member)
        db.session.commit()
        return f"Member created. Member id = {member.id}"
    except Exception as e:
        return str(e)

@app.route("/create/category", methods=['GET', 'POST'])
def create_category():
    if request.method == 'GET':
        return render_template("create_category.html", now=now, site=site)
    name = request.form.get('name')
    amount = request.form.get('amount')
    try:
        category = Category(name, amount)
        db.session.add(category)
        db.session.commit()
        return f"Category add. Category id = {category.id}"
    except Exception as e:
        return str(e)

@app.route("/create/contribution", methods=['GET', 'POST'])
def create_contribution():
    if request.method == 'GET':
        years = ['2020', '2019', '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', '2010', '2009', '2008', '2007']
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August', 'September', 'October', 'November', 'December']
        return render_template("create_contribution.html", now=now, site=site, months=months, years=years)
    year = request.form.get('year')
    month = request.form.get('month')
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # return redirect(url_for('uploaded_file', filename=filename))
        try:
            with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                lines = 0
                lines_processed = 0
                lines_invalid = 0
                lines_valid = 0
                for row in csv_reader:
                    if row[0] and row[1]:
                        email = row[0].strip()
                        amount = row[1].strip()
                        invalid = True
                        if check_email(email):
                            member = get_member_by_email(email)
                            # if member and member.category.amount == amount:
                            if member:
                                try: 
                                    amount_numeric = float(amount)
                                    category = get_category(member.category)
                                    site['errors'].append(f"Category: {category}")
                                    if amount_numeric != float(category.amount):
                                        raise ValueError
                                    contribution = ValidContribution(year, month, member.email, amount_numeric)
                                    db.session.add(contribution)
                                    db.session.commit()
                                    invalid = False
                                    lines_valid += 1
                                except ValueError as e:
                                    site['errors'].append(str(e))
                        if invalid:
                            contribution = Contribution(year, month, email, amount)
                            db.session.add(contribution)
                            db.session.commit()
                            lines_invalid += 1
                        lines_processed += 1
                    lines += 1
            if lines_invalid < 1:
                site['errors'].append(f"Success. {lines_valid}/{lines} records valid.")
                return render_template('index.html', now=now, site=site)
            else:
                site['errors'].append(f"Success. {lines_invalid}/{lines} records invalid.")
                return render_template('index.html', now=now, site=site)
        except Exception as e:
            site['errors'].append(str(e))
            return render_template('index.html', now=now, site=site)
    site['errors'].append('Invalid file type.')
    return render_template('create_contribution.html', now=now, site=site)

@app.route("/markaspaid/<email>", methods=['GET', 'POST'])
def mark_as_paid(email):
    site["errors"].append(f"That funtionality will be added soon")
    return render_template('index.html', now=now, site=site)

@app.route('/upload/csv', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))

def get_member_by_email(email_):
    try:
        member = Member.query.filter_by(email=email_).first()
        return member
    except Exception:
        return False
def get_category(id_):
    try:
        category = Category.query.filter_by(id=id_).first()
        return category
    except Exception:
        return False

def get_valid_contributions():
    try:
        valid_contributions = ValidContribution.query.all()
        return valid_contributions
    except Exception as e:
        site['errors'].append(str(e))
        return False

def get_invalid_contributions():
    try:
        invalid_contributions = Contribution.query.all()
        return invalid_contributions
    except Exception as e:
        site['errors'].append(str(e))
        return False

def get_categories():
    try:
        categories = Category.query.all()
        return categories
    except Exception as e:
        site['errors'].append(str(e))
        return False

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_email(email):
    # return validate_email(email, verify=True)
    return re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email) != 'None'

if __name__ == '__main__':
    app.run()