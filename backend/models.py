from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')
    filters = db.Column(db.String) 

    records = db.relationship('SalesRecord', backref='task', lazy=True)

class SalesRecord(db.Model):
    __tablename__ = 'sales_records'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    company = db.Column(db.String(50))
    car_model = db.Column(db.String(50))
    sale_date = db.Column(db.Date)
    price = db.Column(db.Float)
