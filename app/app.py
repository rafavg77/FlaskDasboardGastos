from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import logging
import os
from config.config import ProductionConfig, DevelopmentConfig, TestingConfig
from db import db

logging.basicConfig(filename='app.log', level=logging.DEBUG)

app = Flask(__name__)

app.config['FLASK_ENV'] = os.getenv('FLASK_ENV')

if app.config['FLASK_ENV'] == 'production':
    app.config.from_object(ProductionConfig)
elif app.config['FLASK_ENV'] == 'testing':
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(DevelopmentConfig)


bcrypt = Bcrypt(app)

from models.user import User
from models.account import Account
from models.transaction import Transaction

app.app_context().push()

# Crear una instancia de LoginManager
login_manager = LoginManager()
#login_manager.login_view = 'dashboard'
login_manager.init_app(app)



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

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, host = '0.0.0.0', debug=True)
