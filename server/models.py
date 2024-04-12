from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.exc import IntegrityError

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    phone_number = Column(String(10), nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name is required.")
        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number

class Post(db.Model):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    summary = Column(String(250), nullable=False)
    content = Column(String(1000), nullable=False)
    category = Column(Enum('Fiction', 'Non-Fiction'), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    @validates('title')
    def validate_title(self, key, title):
        if not any(word in title for word in ["Won't Believe", "Secret", "Top", "Guess"]):
            raise ValueError("Title must contain one of the specified words.")
        return title

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Summary must be a maximum of 250 characters.")
        return summary

    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Content must be at least 250 characters long.")
        return content

    @validates('category')
    def validate_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return category