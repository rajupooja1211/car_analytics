from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_app import app, db
from flask_app import Task, SalesRecord
from flask_cors import CORS
from datetime import datetime

from collections import defaultdict

import json

# Set up Flask
app = Flask(__name__)
CORS(app)  # Allow requests from Postman/browser


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Models
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='pending')
    filters = db.Column(db.String)

class SalesRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    company = db.Column(db.String(50))
    car_model = db.Column(db.String(50))
    sale_date = db.Column(db.Date)
    price = db.Column(db.Float)

# Routes
@app.route("/", methods=["GET"])
def home():
    return "Backend is running!"

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    filters = json.dumps(data.get("filters", {}))

    new_task = Task(filters=filters, status="pending")
    db.session.add(new_task)
    db.session.commit()
    print(f"🟢 Task {new_task.id} created. Starting queue...")
    from job_queue import add_to_queue
    add_to_queue(new_task.id, filters)


    return jsonify({"message": "Task created", "task_id": new_task.id}), 201
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
   

    return jsonify({
        "id": task.id,
        "created_at": task.created_at,
        "status": task.status,
        "filters": json.loads(task.filters)
    })
@app.route("/analytics/<int:task_id>", methods=["GET"])
def task_analytics(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    if task.status != "completed":
        return jsonify({"message": "Task not completed yet"}), 202

    records = SalesRecord.query.filter_by(task_id=task_id).all()

    sales_by_company = defaultdict(float)
    records_by_year = defaultdict(int)

    for record in records:
        year = record.sale_date.year
        sales_by_company[record.company] += record.price
        records_by_year[year] += 1

    return jsonify({
        "sales_by_company": sales_by_company,
        "records_by_year": records_by_year
    })

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5001)
