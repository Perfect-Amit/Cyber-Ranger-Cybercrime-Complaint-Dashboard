from app import app
from database import init_db

init_db(app)
print("Database initialized successfully!")