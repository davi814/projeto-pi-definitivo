from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(20))
    
    cep = db.Column(db.String(9))
    address = db.Column(db.String(200))
    neighborhood = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(2))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    professional = db.relationship('Professional', backref='user', uselist=False, cascade='all, delete-orphan')
    service_requests = db.relationship('ServiceRequest', backref='client', lazy=True, cascade='all, delete-orphan')
    reviews_given = db.relationship('Review', foreign_keys='Review.client_id', backref='client', lazy=True, cascade='all, delete-orphan')

class ServiceCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(50))
    description = db.Column(db.Text)
    
    professionals = db.relationship('Professional', backref='category', lazy=True)

class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    category_id = db.Column(db.Integer, db.ForeignKey('service_category.id'), nullable=False)
    
    bio = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    starting_price = db.Column(db.Float)
    profile_photo = db.Column(db.String(200))
    
    verified = db.Column(db.Boolean, default=False)
    response_time = db.Column(db.String(50))
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    service_requests = db.relationship('ServiceRequest', backref='professional', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='professional', lazy=True, cascade='all, delete-orphan')
    
    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        return sum(r.rating for r in self.reviews) / len(self.reviews)
    
    @property
    def review_count(self):
        return len(self.reviews)

class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float)
    preferred_date = db.Column(db.String(100))
    
    status = db.Column(db.String(20), default='pending')
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey('professional.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
