from flask_app import app, db, Task, SalesRecord
import threading
import json
import pandas as pd
from datetime import datetime

def simulate_job(task_id, filters):
    with app.app_context():
        print(f"Starting job for Task ID: {task_id}")
        try:
            task = Task.query.get(task_id)
            task.status = 'in progress'
            db.session.commit()
            print("Task marked as in progress")

            with open('data/sourceA.json') as f:
                data_a = json.load(f)
            df_a = pd.DataFrame(data_a)

            df_b = pd.read_csv('data/sourceB.csv')

            df = pd.concat([df_a, df_b], ignore_index=True)

            filters = json.loads(filters)
            start = int(filters.get("start_year", 2000))
            end = int(filters.get("end_year", 2100))
            companies = filters.get("companies", [])

            df['sale_date'] = pd.to_datetime(df['sale_date'])
            df = df[(df['sale_date'].dt.year >= start) & (df['sale_date'].dt.year <= end)]
            if companies:
                df = df[df['company'].isin(companies)]

            print(f"Filtered {len(df)} records")

            for _, row in df.iterrows():
                rec = SalesRecord(
                    task_id=task_id,
                    company=row['company'],
                    car_model=row['car_model'],
                    sale_date=row['sale_date'],
                    price=row['price']
                )
                db.session.add(rec)

            task.status = 'completed'
            db.session.commit()
            print(f"Task {task_id} marked as completed")

        except Exception as e:
            task.status = f'error: {str(e)}'
            db.session.commit()
            print(f"Task {task_id} failed: {str(e)}")

def add_to_queue(task_id, filters):
    print(f"Queuing task {task_id}")
    thread = threading.Thread(target=simulate_job, args=(task_id, filters))
    thread.start()
