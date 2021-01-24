from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy import update, delete
from flask_login import login_required, current_user

from . import db
from . import firebase, firebase_db

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
    items_fb = firebase_db.child("shoppinglists/"+str(current_user.id)+"/items")
    items = items_fb.get()
    if request.method == 'GET':
        # If shoppinglist exists, display the current contents
        if items.val():
            return render_template(
                'shoppinglist.html',
                shoppinglist=items.val(),
                )
        else:
            return render_template(
                'shoppinglist.html',
                shoppinglist={},
                )
    else:
        new_item = {
            "name": request.form.get("name"),
            "quantity": request.form.get("quantity"),
            "expirationDate": request.form.get("expirationDate"),
        }
        # Make shoppinglist if it does not exist
        if not items.val():
            firebase_db.child("shoppinglists/"+str(current_user.id)).push(data={"owner": current_user.id})

        items_fb = firebase_db.child("shoppinglists/"+str(current_user.id)+"/items")
        items_fb.push(data=new_item)
        return redirect(
            url_for('main.shoppinglist')
            )

# @main.route('/shoppinglist/edit', methods=['POST'])
# @login_required
# def shoppinglist_edit():
#     update_item
#     shoppinglist_path = '/shoppinglists/'+str(current_user.id)
#     shoppinglist = firebase_db.child("shoppinglists").child(str(current_user.id)).get()
#     if request.method == 'POST':
#         firebase_db.child("shoppinglists").push(data=update_item)

@main.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    inventory_fb = firebase_db.child("inventory/"+str(current_user.id))
    inventory = inventory_fb.get()
    if request.method == 'GET':
        # If inventory exists, display the current contents
        if inventory.val():
            return render_template(
                'inventory.html',
                shoppinglist=inventory.val(),
                )
        else:
            return render_template(
                'inventory.html',
                )
    else:
        # If inventory exists, add new item to shopping list
        newitem = {
            "name": request.form.get("name"),
            "quantity": request.form.get("quantity"),
            "expirationDate": request.form.get("expirationDate"),
        }
        inventory_fb.push(data=newitem)
        return redirect(
            url_for('main.shoppinglist')
            )
