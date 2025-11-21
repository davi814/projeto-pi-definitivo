from database import db
from flask_login import UserMixin
from datetime import datetime

# ---------------------------------------------------
# USER MODEL
# ---------------------------------------------------
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)

    password_hash = db.Column(db.String(255), nullable=False)

    user_type = db.Column(db.String(20), nullable=False)  # "client" ou "professional"

    cep = db.Column(db.String(8), nullable=False)
    address = db.Column(db.String(200), nullable=True)
    neighborhood = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(2), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    professional_profile = db.relationship("Professional", backref="user", uselist=False)
    client_requests = db.relationship("ServiceRequest", backref="client", foreign_keys="ServiceRequest.client_id")

    def __repr__(self):
        return f"<User {self.name}>"


# ---------------------------------------------------
# CATEGORIAS DE SERVIÇO
# ---------------------------------------------------
class ServiceCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    professionals = db.relationship("Professional", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


# ---------------------------------------------------
# PERFIL PROFISSIONAL
# ---------------------------------------------------
class Professional(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    category_id = db.Column(db.Integer, db.ForeignKey("service_category.id"), nullable=False)

    bio = db.Column(db.Text, nullable=True)
    experience_years = db.Column(db.Integer, nullable=False)
    starting_price = db.Column(db.Float, nullable=False)
    response_time = db.Column(db.String(50), default="24 horas")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    service_requests = db.relationship("ServiceRequest", backref="professional", lazy=True)

    def __repr__(self):
        return f"<Professional {self.user.name}>"


# ---------------------------------------------------
# PEDIDOS DE SERVIÇOS (CLIENTE → PROFISSIONAL)
# ---------------------------------------------------
class ServiceRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    client_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional.id"), nullable=False)

    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending")  # pending / accepted / finished

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    review = db.relationship("Review", backref="service_request", uselist=False)

    def __repr__(self):
        return f"<Request {self.id} - Status {self.status}>"


# ---------------------------------------------------
# AVALIAÇÕES / REVIEWS
# ---------------------------------------------------
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    request_id = db.Column(db.Integer, db.ForeignKey("service_request.id"), nullable=False)

    rating = db.Column(db.Integer, nullable=False)  # 1 a 5 estrelas
    comment = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review {self.rating} stars>"# models.py
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
    cpf = db.Column(db.String(14), unique=True, nullable=False)   # formato 000.000.000-00
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    password_hash = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False, default='client')  # 'client' ou 'professional'

    cep = db.Column(db.String(9), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    neighborhood = db.Column(db.String(120), nullable=True)
    city = db.Column(db.String(120), nullable=True)
    state = db.Column(db.String(2), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    professional_profile = db.relationship('Professional', backref='user', uselist=False, cascade='all, delete-orphan')
    client_requests = db.relationship('ServiceRequest', backref='client', foreign_keys='ServiceRequest.client_id', cascade='all, delete-orphan')
    reviews_given = db.relationship('Review', foreign_keys='Review.client_id', backref='client', cascade='all, delete-orphan')

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

    professionals = db.relationship('Professional', backref='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Category {self.name}>"


# -------------------------
# PROFESSIONAL
# -------------------------
class Professional(db.Model):
    __tablename__ = 'professionals'
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('service_categories.id'), nullable=True)

    bio = db.Column(db.Text, nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)
    starting_price = db.Column(db.Float, nullable=True)   # valor numérico
    profile_photo = db.Column(db.String(255), nullable=True)

    verified = db.Column(db.Boolean, default=False)
    response_time = db.Column(db.String(50), nullable=True, default='24 horas')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    service_requests = db.relationship('ServiceRequest', backref='professional', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='professional', cascade='all, delete-orphan')

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

    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    budget = db.Column(db.Float, nullable=True)
    preferred_date = db.Column(db.String(100), nullable=True)

    status = db.Column(db.String(40), default='pendente')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Request {self.id} status={self.status}>"


# -------------------------
# REVIEW
# -------------------------
class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)

    professional_id = db.Column(db.Integer, db.ForeignKey('professionals.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    rating = db.Column(db.Integer, nullable=False)  # 1..5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Review {self.id} rating={self.rating}>"

