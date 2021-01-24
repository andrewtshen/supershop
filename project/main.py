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
    personal_shoppinglist = '/shoppinglist/'+str(current_user.id)
    if request.method == 'GET':
        shoppinglist = firebase.get(personal_shoppinglist, None)

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
        newitem = {
            "name": request.form.get("name"),
            "quantity": request.form.get("quantity"),
            "expirationDate": request.form.get("expirationDate"),
        }
        ret = firebase.get(personal_shoppinglist, None)
        firebase.post(personal_shoppinglist, data=newitem)
        return redirect(
            url_for('main.shoppinglist')
            )


    # if request.method == 'GET':
    #     ret = firebase.get('/1', None)
    #     if ret:
    #         return ret
    #     else:
    #         return "Shopping list not found"
    # else:
    #     itemdata = dict(request.form)
    #     isPurchased = False
    #     name = itemdata.name
    #     quantity = itemdata.quantity
    #     newitem = {
    #         "name": name,
    #         "isPurchased": isPurchased,
    #         "quantity": quantity,
    #     }
    #     firebase.push('/1', newitem)

@main.route('/test')
@login_required
def test():
    isPurchased = False
    name = "Oranges"
    quantity = 8
    newitem = {
        "name": name,
        "isPurchased": isPurchased,
        "quantity": quantity,
    }
    ret = firebase.post('shoppinglist/item', data=newitem)
    return ret

