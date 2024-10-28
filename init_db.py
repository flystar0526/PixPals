from models import db
from app import app

with app.app_context():
    print("Initializing the database...")
    db.create_all()
    print("Database initialization complete!")
