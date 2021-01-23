from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import update, delete
from flask_login import login_required, current_user
from .models import Group, User_Group

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

@main.route('/mygroups')
@login_required
def mygroups():
    groups = Group.query.all()
    return render_template(
            'mygroups.html',
            groups=groups
            )

@main.route('/mygroups/<int:group_id>')
@login_required
def mygroup_id(group_id=1):
    group = Group.query.get(int(group_id))
    return render_template(
            'group.html',
            group_name=group.name,
            name=current_user.name,
            is_set_favorite_drink=current_user.is_set_favorite_drink,
            favorite_drink=current_user.favorite_drink,
            )

@main.route('/makegroup', methods=['GET'])
@login_required
def make_group():
    return render_template(
            'makegroup.html',
            )

@main.route('/makegroup', methods=['POST'])
@login_required
def make_group_post():
    # Get all of the info to make the group
    name = request.form.get('name')
    new_group = Group(name=name)
    db.session.add(new_group)
    db.session.commit()

    # Get add yourself to the user_group combination
    group_id = new_group.group_id
    user_id = current_user.id
    new_user_group = User_Group(user_id=user_id, group_id=group_id)

    return redirect(url_for('main.mygroups'))

@main.route('/joingroup')
@login_required
def join_group():
    return 'Join a Group',
