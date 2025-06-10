import sqlite3
from flask import *

def init_db(app):
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        
        # Create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                crime_type TEXT NOT NULL,
                description TEXT,
                location TEXT,
                date TEXT NOT NULL,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        db.commit()

def get_db(app):
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def add_complaint(crime_type, description, location, date, status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        INSERT INTO complaints (crime_type, description, location, date, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (crime_type, description, location, date, status))
    db.commit()

def get_all_complaints():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM complaints ORDER BY date DESC')
    return cursor.fetchall()

def get_complaints_by_type(crime_type):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM complaints WHERE crime_type = ? ORDER BY date DESC', (crime_type,))
    return cursor.fetchall()