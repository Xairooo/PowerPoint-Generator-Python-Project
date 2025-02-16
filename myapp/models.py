from flask_login import UserMixin
from database import db
from dataclasses import dataclass
from typing import List, Optional

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


@dataclass
class BulletPointsSection:
    """Represents a bullet points content section in a slide layout"""
    position: str  # Layout position (e.g., "body", "left-column", etc.)
    items: List[str]  # List of bullet point text items
    # type: str = "bullets"  # Explicit type identifier for JSON parsing

@dataclass
class ImageSection:
    """Represents an image content section in a slide layout"""
    position: str  # Layout position (e.g., "right-column", "body", etc.)
    description: str  # Path to image file or URL
    type: str = "image"  # Explicit type identifier for JSON parsing
    caption: Optional[str] = None  # Optional image caption
    width: Optional[int] = None  # Optional custom width in pixels
    height: Optional[int] = None  # Optional custom height in pixels

@dataclass
class TextSection:
    """Represents an image content section in a slide layout"""
    position: str  # Layout position (e.g., "right-column", "body", etc.)
    content: str  # Path to image file or URL
    type: str = "text"  # Explicit type identifier for JSON parsing
