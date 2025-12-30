# server/models.py
from flask_sqlalchemy import SQLAlchemy # type: ignore
from sqlalchemy.orm import validates
import re

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # --- Author Validations ---

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Author must have a name.")
        
        # Manually check for uniqueness to satisfy the Python-side validation test
        # We query the database to see if an author with this name already exists
        author = Author.query.filter_by(name=name).first()
        if author:
            raise ValueError("No two authors have the same name.")
            
        return name

    @validates('phone_number')
    def validate_phone(self, key, phone_number):
        if not (len(phone_number) == 10 and phone_number.isdigit()):
            raise ValueError("Phone number must be exactly ten digits.")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # --- Post Validations ---

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Post must have a title.")
        
        clickbait_keywords = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in title for word in clickbait_keywords):
            raise ValueError("Title must be clickbait-y.")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary) > 250:
            raise ValueError("Summary must be a maximum of 250 characters.")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'.")
        return category

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title})'