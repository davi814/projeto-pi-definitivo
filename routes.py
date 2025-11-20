from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User, ServiceCategory, Professional, ServiceRequest, Review
from validate_docbr import CPF
import requests

cpf_validator = CPF()

def validate_cep(cep):
    cep_clean = cep.replace('-', '').replace('.', '')
    if len(cep_clean) != 8:
        return None
    
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep_clean}/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if 'erro' not in data:
                return {
                    'cep': cep_clean,
                    'address': data.get('logradouro', ''),
                    'neighborhood': data.get('bairro', ''),
                    'city': data.get('localidade', ''),
                    'state': data.get('uf', '')
                }
    except:
        pass
    return None

@app.route('/')
def index():
    categories = ServiceCategory.query.all()
    professionals = Professional.query.order_by(Professional.created_at.desc()).limit(6).all()
    return render_template('index.html', categories=categories, professionals=professionals)

@app.route('/registro', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        cpf = request.form.get('cpf')
        password = request.form.get('password')
        user_type = request.form.get('user_type')
        phone = request.form.get('phone')
        cep = request.form.get('cep')
        
        if not cpf_validator.validate(cpf):
            flash('CPF inválido', 'error')
            return render_template('register.html')
        
        cep_data = validate_cep(cep)
        if not cep_data:
            flash('CEP inválido', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email já cadastrado', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(cpf=cpf).first():
            flash('CPF já cadastrado', 'error')
            return render_template('register.html')
        
        user = User(
            name=name,
            email=email,
            cpf=cpf,
            password_hash=generate_password_hash(password),
            user_type=user_type,
            phone=phone,
            cep=cep_data['cep'],
            address=cep_data['address'],
            neighborhood=cep_data['neighborhood'],
            city=cep_data['city'],
            state=cep_data['state']
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        
        if user_type == 'professional':
            flash('Cadastro realizado com sucesso! Complete seu perfil profissional.', 'success')
            return redirect(url_for('complete_professional_profile'))
        
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/completar-perfil-profissional', methods=['GET', 'POST'])
@login_required
def complete_professional_profile():
    if current_user.user_type != 'professional':
        return redirect(url_for('index'))
    
    if Professional.query.filter_by(user_id=current_user.id).first():
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        category_id = request.form.get('category_id')
        bio = request.form.get('bio')
        experience_years = request.form.get('experience_years')
        starting_price = request.form.get('starting_price')
        
        professional = Professional(
            user_id=current_user.id,
            category_id=category_id,
            bio=bio,
            experience_years=experience_years,
            starting_price=starting_price,
            response_time='24 horas'
        )
        
        db.session.add(professional)
        db.session.commit()
        
        flash('Perfil profissional criado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    categories = ServiceCategory.query.all()
    return render_template('complete_profile.html', categories=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        
        flash('Email ou senha inválidos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/buscar')
def search():
    category_id = request.args.get('category')
    city = request.args.get('city')
    
    query = Professional.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if city:
        query = query.join(User).filter(User.city.ilike(f'%{city}%'))
    
    professionals = query.all()
    categories = ServiceCategory.query.all()
    
    return render_template('search.html', professionals=professionals, categories=categories)

@app.route('/profissional/<int:professional_id>')
def professional_profile(professional_id):
    professional = Professional.query.get_or_404(professional_id)
    reviews = Review.query.filter_by(professional_id=professional_id).order_by(Review.created_at.desc()).limit(10).all()
    return render_template('professional_profile.html', professional=professional, reviews=reviews)

@app.route('/solicitar-orcamento/<int:professional_id>', methods=['GET', 'POST'])
@login_required
def request_service(professional_id):
    if current_user.user_type != 'client':
        flash('Apenas clientes podem solicitar orçamentos', 'error')
        return redirect(url_for('index'))
    
    professional = Professional.query.get_or_404(professional_id)
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        budget = request.form.get('budget')
        preferred_date = request.form.get('preferred_date')
        
        service_request = ServiceRequest(
            client_id=current_user.id,
            professional_id=professional_id,
            title=title,
            description=description,
            budget=budget,
            preferred_date=preferred_date
        )
        
        db.session.add(service_request)
        db.session.commit()
        
        flash('Solicitação enviada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('request_service.html', professional=professional)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'professional':
        professional = Professional.query.filter_by(user_id=current_user.id).first()
        if not professional:
            return redirect(url_for('complete_professional_profile'))
        
        requests = ServiceRequest.query.filter_by(professional_id=professional.id).order_by(ServiceRequest.created_at.desc()).all()
        return render_template('dashboard_professional.html', professional=professional, requests=requests)
    else:
        requests = ServiceRequest.query.filter_by(client_id=current_user.id).order_by(ServiceRequest.created_at.desc()).all()
        return render_template('dashboard_client.html', requests=requests)

@app.route('/atualizar-status/<int:request_id>', methods=['POST'])
@login_required
def update_request_status(request_id):
    service_request = ServiceRequest.query.get_or_404(request_id)
    
    if current_user.user_type == 'professional':
        professional = Professional.query.filter_by(user_id=current_user.id).first()
        if service_request.professional_id != professional.id:
            flash('Acesso negado', 'error')
            return redirect(url_for('dashboard'))
    elif service_request.client_id != current_user.id:
        flash('Acesso negado', 'error')
        return redirect(url_for('dashboard'))
    
    new_status = request.form.get('status')
    service_request.status = new_status
    db.session.commit()
    
    flash('Status atualizado com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/avaliar/<int:professional_id>', methods=['GET', 'POST'])
@login_required
def review_professional(professional_id):
    if current_user.user_type != 'client':
        flash('Apenas clientes podem avaliar profissionais', 'error')
        return redirect(url_for('index'))
    
    professional = Professional.query.get_or_404(professional_id)
    
    if request.method == 'POST':
        rating = request.form.get('rating')
        comment = request.form.get('comment')
        
        existing_review = Review.query.filter_by(
            professional_id=professional_id,
            client_id=current_user.id
        ).first()
        
        if existing_review:
            flash('Você já avaliou este profissional', 'error')
            return redirect(url_for('professional_profile', professional_id=professional_id))
        
        review = Review(
            professional_id=professional_id,
            client_id=current_user.id,
            rating=rating,
            comment=comment
        )
        
        db.session.add(review)
        db.session.commit()
        
        flash('Avaliação enviada com sucesso!', 'success')
        return redirect(url_for('professional_profile', professional_id=professional_id))
    
    return render_template('review.html', professional=professional)

@app.route('/api/validar-cep/<cep>')
def api_validate_cep(cep):
    cep_data = validate_cep(cep)
    if cep_data:
        return jsonify(cep_data)
    return jsonify({'error': 'CEP inválido'}), 400
