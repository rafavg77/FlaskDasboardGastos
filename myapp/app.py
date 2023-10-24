from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import logging
import datetime
import os
from config.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig


logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)

app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')

if app.config['FLASK_ENV'] == 'production':
    app.config.from_object(ProductionConfig)
elif app.config['FLASK_ENV'] == 'testing':
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.app_context().push()

# Crear una instancia de LoginManager
login_manager = LoginManager()
#login_manager.login_view = 'dashboard'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    accounts = db.relationship('Account', backref='user', lazy=True)
    #transactions = db.relationship('Transaction', backref='user', lazy=True)

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50), nullable=False)
    alias = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    transactions = db.relationship('Transaction', backref='user', lazy=True)

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transaction_date = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    description = db.Column(db.String(255))
    ingress = db.Column(db.Float(precision=2))
    engress = db.Column(db.Float(precision=2))
    comment = db.Column(db.String(255))
    status = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())


@login_manager.user_loader
def load_user(user_id):
    # Debes implementar esta función para cargar usuarios desde la base de datos.
    # Retorna el usuario correspondiente al 'user_id' o None si no se encuentra.
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('El usuario ya existe', 'danger')
        else:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = User(username=username, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # El usuario ha iniciado sesión correctamente
            # Aquí deberías implementar el manejo de sesiones
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Credenciales incorrectas', 'danger')
    return render_template('login.html')

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

# Define el modelo de datos Account aquí...

@app.route('/accounts', methods=['GET'])
def list_accounts():
    accounts = Account.query.all()
    return render_template('cuentas/cuenta_lista.html',accounts=accounts)

@app.route('/accounts/create', methods=['GET', 'POST'])
@login_required
def create_account():
    if request.method == 'POST':
        institution = request.form.get('institution')
        account_type = request.form.get('account_type')
        alias = request.form.get('alias')
        user_id = session.get('_user_id') # Define el usuario al que pertenece la cuenta (puedes obtenerlo de la sesión o de donde sea necesario)

        account = Account(institution=institution, account_type=account_type, alias=alias, user_id=user_id)
        db.session.add(account)
        db.session.commit()
        flash('Cuenta creada exitosamente', 'success')
        return redirect(url_for('list_accounts'))

    return render_template('cuentas/cuenta_crear.html')

@app.route('/accounts/update/<int:id>', methods=['GET', 'POST'])
def update_account(id):
    account = Account.query.get(id)

    if request.method == 'POST':
        institution = request.form.get('institution')
        account_type = request.form.get('account_type')
        alias = request.form.get('alias')

        user_id = session.get('_user_id')

        account.institution = institution
        account.account_type = account_type
        account.alias = alias
        account.user_id = user_id


        db.session.commit()
        flash('Cuenta actualizada exitosamente', 'success')
        return redirect(url_for('list_accounts'))

    return render_template('cuentas/cuenta_actualiza.html', account=account)

@app.route('/accounts/delete/<int:id>', methods=['POST'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    flash('Cuenta eliminada exitosamente', 'success')
    return redirect(url_for('list_accounts'))

@app.route('/movimientos')
@login_required
def movimientos():
    return render_template('movimientos.html')

@app.route('/presupuesto')
@login_required
def presupuesto():
    return render_template('presupuesto.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
