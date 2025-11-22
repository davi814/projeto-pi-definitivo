# models.py
from database import db
from flask_login import UserMixin
from datetime import datetime

# -------------------------
# USERS
# -------------------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='client')

    cep = db.Column(db.String(9), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    neighborhood = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(2), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # RELACIONAMENTOS
    professional_profile = db.relationship(
        'Professional',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan'
    )

    client_requests = db.relationship(
        'ServiceRequest',
        backref='client',
        foreign_keys='ServiceRequest.client_id',
        cascade='all, delete-orphan'
    )

    reviews_given = db.relationship(
        'Review',
        backref='client',
        foreign_keys='Review.client_id',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<User {self.id} {self.name}>"


# -------------------------
# SERVICE CATEGORY
# -------------------------
class ServiceCategory(db.Model):
    __tablename__ = 'service_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    professionals = db.relationship(
        'Professional',
        backref='category',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Category {self.name}>"


# -------------------------
# PROFESSIONAL
# -------------------------
class Professional(db.Model):
    __tablename__ = 'professionals'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'))

    bio = db.Column(db.Text, nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    starting_price = db.Column(db.Float, nullable=True)
    profile_photo = db.Column(db.String(255), nullable=True)

    verified = db.Column(db.Boolean, default=False)
    response_time = db.Column(db.String(50), default='24 horas')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    service_requests = db.relationship(
        'ServiceRequest',
        backref='professional',
        cascade='all, delete-orphan'
    )

    reviews = db.relationship(
        'Review',
        backref='professional',
        cascade='all, delete-orphan'
    )

    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        total = sum(r.rating for r in self.reviews)
        return total / len(self.reviews)

    @property
    def review_count(self):
        return len(self.reviews)

    def __repr__(self):
        return f"<Professional {self.id} - user {self.user_id}>"


# -------------------------
# SERVICE REQUEST
# -------------------------
class ServiceRequest(db.Model):
    __tablename__ = 'service_requests'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)

    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    budget = db.Column(db.Float)
    preferred_date = db.Column(db.String(100))

    status = db.Column(db.String(40), default='pendente')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    review = db.relationship(
        'Review',
        backref='service_request',
        uselist=False,
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<Request {self.id} status={self.status}>"


# -------------------------
# REVIEW (AGORA VINCULADO A ServiceRequest)
# -------------------------
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)

    request_id = db.Column(db.Integer, db.ForeignKey('service_requests.id'), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review {self.id} rating={self.rating}>"
