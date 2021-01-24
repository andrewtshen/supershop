from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory
from sqlalchemy import update, delete
from flask_login import login_required, current_user
from datetime import datetime
import os

from app import db, firebase, firebase_db

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

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

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
        if not firebase_db.child("shoppinglists/"+str(current_user.id)).get().val():
            firebase_db.child("shoppinglists/"+str(current_user.id)).push(data={"owner": current_user.id})

        firebase_db.child("shoppinglists/"+str(current_user.id)+"/items").push(data=new_item)
        return redirect(
            url_for('main.shoppinglist')
            )

@main.route('/shoppinglist/edit', methods=['POST'])
@login_required
def shoppinglist_edit():
    old_name = request.form.get("hidden")
    new_name = request.form.get("name")

    for val in firebase_db.child("shoppinglists/"+str(current_user.id)+"/items").get().val():
        if firebase_db.child("shoppinglists/"+str(current_user.id)+"/items/"+val).get().val()['name'] == old_name:
            firebase_db.child("shoppinglists/"+str(current_user.id)+"/items/"+val).update({
                "name": new_name,
                "quantity": request.form.get("quantity"),
            })
    return redirect(
        url_for('main.shoppinglist')
        )

@main.route('/shoppinglist/remove', methods=['POST'])
@login_required
def shoppinglist_remove():
    name = request.form.get("name")
    for val in firebase_db.child("shoppinglists/"+str(current_user.id)+"/items").get().val():
        if firebase_db.child("shoppinglists/"+str(current_user.id)+"/items/"+val).get().val()['name'] == name:
            firebase_db.child("shoppinglists/"+str(current_user.id)+"/items/"+val).remove()
    return redirect(
        url_for('main.shoppinglist')
        )

@main.route('/shoppinglist/addtoinventory', methods=['POST'])
@login_required
def shoppinglist_addtoinventory():
    name = request.form.get("name")
    quantity = request.form.get("quantity")
    for val in firebase_db.child("shoppinglists/"+str(current_user.id)+"/items").get().val():
        if firebase_db.child("shoppinglists/"+str(current_user.id)+"/items/"+val).get().val()['name'] == name:
            firebase_db.child("shoppinglists/"+str(current_user.id)+"/items/"+val).remove()
            if not firebase_db.child("inventories/"+str(current_user.id)).get().val():
                firebase_db.child("inventories/"+str(current_user.id)).push(data={"owner": current_user.id})

            new_item = {
                "name": name,
                "quantity": quantity,
                "expirationDate": datetime.today().strftime('%Y-%m-%d'),
                "datePurchased": datetime.today().strftime('%Y-%m-%d'),
            }

            firebase_db.child("inventories/"+str(current_user.id)+"/items").push(data=new_item)

    return redirect(
        url_for('main.shoppinglist')
        )

@main.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    items_fb = firebase_db.child("inventories/"+str(current_user.id)+"/items")
    items = items_fb.get()
    if request.method == 'GET':
        # If shoppinglist exists, display the current contents
        if items.val():
            return render_template(
                'inventory.html',
                inventory=items.val(),
                )
        else:
            return render_template(
                'inventory.html',
                inventory={},
                )
    else:
        new_item = {
            "name": request.form.get("name"),
            "quantity": request.form.get("quantity"),
            "expirationDate": request.form.get("expirationDate"),
        }
        # Make shoppinglist if it does not exist
        if not firebase_db.child("inventories/"+str(current_user.id)).get().val():
            firebase_db.child("inventories/"+str(current_user.id)).push(data={"owner": current_user.id})

        firebase_db.child("inventories/"+str(current_user.id)+"/items").push(data=new_item)
        return redirect(
            url_for('main.inventory')
            )

@main.route('/inventory/edit', methods=['POST'])
@login_required
def inventory_edit():
    old_name = request.form.get("hidden")
    new_name = request.form.get("name")

    for val in firebase_db.child("inventories/"+str(current_user.id)+"/items").get().val():
        if firebase_db.child("inventories/"+str(current_user.id)+"/items/"+val).get().val()['name'] == old_name:
            firebase_db.child("inventories/"+str(current_user.id)+"/items/"+val).update({
                "name": new_name,
                "quantity": request.form.get("quantity"),
                "expirationDate": request.form.get("expirationDate"),
                "datePurchased": request.form.get("datePurchased"),
            })
    return redirect(
        url_for('main.inventory')
        )

@main.route('/inventory/remove', methods=['POST'])
@login_required
def inventory_remove():
    name = request.form.get("name")
    for val in firebase_db.child("inventories/"+str(current_user.id)+"/items").get().val():
        if firebase_db.child("inventories/"+str(current_user.id)+"/items/"+val).get().val()['name'] == name:
            firebase_db.child("inventories/"+str(current_user.id)+"/items/"+val).remove()
    return redirect(
        url_for('main.inventory')
        )