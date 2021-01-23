from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import update, delete
from flask_login import login_required, current_user

from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template(
            'profile.html',
            name=current_user.name,
            favorite_drink=current_user.favorite_drink,
            is_set_favorite_drink=current_user.is_set_favorite_drink,
            )

@main.route('/changeinfo', methods=['GET'])
@login_required
def changeinfo():
    return render_template(
            'changeinfo.html',
            )

@main.route('/changeinfo', methods=['POST'])
@login_required
def changeinfo_post():
    current_user.favorite_drink = request.form.get('favorite_drink')
    current_user.is_set_favorite_drink = True
    db.session.commit()
    return redirect(url_for('main.profile'))

