from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import update, delete
from flask_login import login_required, current_user

from . import db
from . import firebase

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template(
            'profile.html',
            name=current_user.firstName,
            id=current_user.id,
            )

@main.route('/changeinfo', methods=['GET', 'POST'])
@login_required
def changeinfo():
    return "Page is currently down"

@main.route('/shoppinglist', methods=['GET', 'POST'])
@login_required
def shoppinglist():
    shoppinglist_path = '/shoppinglists/'+str(current_user.id)
    if request.method == 'GET':
        shoppinglist = firebase.get(shoppinglist_path+'/items', None)

        # If shoppinglist exists, display the current contents
        if shoppinglist:
            return render_template(
                'shoppinglist.html',
                shoppinglist=shoppinglist,
                )
        else:
            return render_template(
                'shoppinglist.html'
                )
    else:
        shoppinglist = firebase.get(shoppinglist_path, None)
        new_item = {
            "name": request.form.get("name"),
            "quantity": request.form.get("quantity"),
            "expirationDate": request.form.get("expirationDate"),
        }
        # Make shoppinglist if it does not exist
        if not shoppinglist:
            firebase.post(shoppinglist_path, data={"owner": current_user.id})

        firebase.post(shoppinglist_path+'/items', data=new_item)
        return redirect(
            url_for('main.shoppinglist')
            )

@main.route('/shoppinglist/edit', methods=['POST'])
@login_required
def shoppinglist_edit():
    update_item
    shoppinglist_path = '/shoppinglists/'+str(current_user.id)
    shoppinglist = firebase.get(shoppinglist_path)
    if request.method == 'POST':
        firebase.post(shoppinglist_path, data=update_item)

@main.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    inventory_path = '/inventory/'+str(current_user.id)
    if request.method == 'GET':
        inventory = firebase.get(inventory_path, None)

        # If inventory exists, display the current contents
        if inventory:
            return render_template(
                'inventory.html',
                shoppinglist=shoppinglist,
                )
        else:
            return render_template(
                'inventory.html',
                )
    else:
        inventory = firebase.get(inventory_path, None)

        # If inventory exists, add new item to shopping list
        newitem = {
            "name": request.form.get("name"),
            "quantity": request.form.get("quantity"),
            "expirationDate": request.form.get("expirationDate"),
        }
        firebase.post(inventory, data=newitem)
        return redirect(
            url_for('main.shoppinglist')
            )
