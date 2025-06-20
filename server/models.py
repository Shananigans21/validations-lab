# server/models.py

from flask_sqlalchemy import SQLAlchemy
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

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Author name is required.")
        name = name.strip()

        existing = Author.query.filter_by(name=name).first()
        if existing and existing.id != self.id:
            raise ValueError(f"Author with name '{name}' already exists.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not re.fullmatch(r'\d{10}', phone_number or ''):
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

    def __repr__(self):
        return f'<Author id={self.id} name={self.name}>'


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    summary = db.Column(db.String)
    category = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content.strip()) < 250:
            raise ValueError("Content must be at least 250 characters.")
        return content.strip()

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary and len(summary.strip()) > 250:
            raise ValueError("Summary must be at most 250 characters.")
        return summary.strip() if summary else summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be 'Fiction' or 'Non-Fiction'.")
        return category

    @validates('title')
    def validate_title(self, key, title):
        phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in phrases):
            raise ValueError("Title must be clickbait-y.")
        return title.strip()

    def __repr__(self):
        return f'<Post id={self.id} title={self.title}>'
