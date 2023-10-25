from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required

from app import db, bcrypt, login_manager
from .model import Account
from . import account_bp

@account_bp.route('/accounts', methods=['GET'])
def list_accounts():
    accounts = Account.query.all()
    return render_template('account/account_list.html',accounts=accounts)

@account_bp.route('/accounts/create', methods=['GET', 'POST'])
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
        return redirect(url_for('account.list_accounts'))

    return render_template('account/account_create.html')

@account_bp.route('/accounts/update/<int:id>', methods=['GET', 'POST'])
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
        return redirect(url_for('account.list_accounts'))

    return render_template('account/account_update.html', account=account)

@account_bp.route('/accounts/delete/<int:id>', methods=['POST'])
def delete_account(id):
    account = Account.query.get(id)
    db.session.delete(account)
    db.session.commit()
    flash('Cuenta eliminada exitosamente', 'success')
    return redirect(url_for('account.list_accounts'))