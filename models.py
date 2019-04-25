from app import db
from datetime import datetime

class Member(db.Model):
    __tablename__ = 'member'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    other_names = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    contributions = db.relationship('ValidContribution', backref='member', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)

    def __init__(self, first_name, other_names, email, category):
        self.first_name = first_name
        self.other_names = other_names
        self.email = email
        self.category = category

    def __repr__(self):
        return f"Employee({self.id}, {self.first_name}, {self.other_names}, {self.email}, {self.category})"

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'other_names': self.other_names, 
            'email': self.email,
            'created_at': self.created_at,
            'category': self.category,
            'contributions': self.contributions
        }

class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    amount = db.Column(db.Numeric(10,2), unique=False, nullable=False)
    members = db.relationship('Member', backref='categories', lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

    def __repr__(self):
        return f"Category({self.id}, {self.name}, {self.amount}, {self.created_at})"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'members': self.members,
            'created_at': self.created_at
        }

class Contribution(db.Model):
    __tablename__ = 'contribution'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, year, month, email, amount):
        self.email = email
        self.year = year
        self.month = month
        self.amount = amount

    def __repr__(self):
        return f"Contribution({self.id}, {self.year}, {self.month}, {self.email}, {self.amount})"

class ValidContribution(db.Model):
    __tablename__ = 'valid_contribution'

    month = db.Column(db.Integer, nullable=False, primary_key=True)
    year = db.Column(db.Integer, nullable=False, primary_key=True)
    amount = db.Column(db.Numeric(10,2), nullable=True)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    email = db.Column(db.String(250), db.ForeignKey('member.email'), nullable=False, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, year, month, email, amount):
        self.year = year
        self.month = month
        self.amount = amount
        self.email = email

    def __repr__(self):
        return f"ValidContribution({self.email}, {self.year}, {self.month}, {self.amount}, {self.paid})"