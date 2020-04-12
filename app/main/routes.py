"""
    Based on https://github.com/UCLComputerScience/comp0034_flask_login_complete and
    https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog
    Adapted by 17075800
"""

from datetime import datetime
from flask import render_template, Blueprint, request, flash, redirect, url_for, make_response, abort
from flask_login import login_required, current_user
from sqlalchemy import or_
from app import db
from app.models import Item
from app.auth.forms import UpdateAccountForm, ItemForm


bp_main = Blueprint('main', __name__)


@bp_main.route("/")
def index():
    return render_template('index.html')


@bp_main.route("/items")
def home():
    items = Item.query.all()
    return render_template('items.html', items=items)


@bp_main.route('/about', methods=['GET'])
def about():
    return render_template("about.html")


@bp_main.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
    return render_template("account.html", form=form)


@bp_main.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        term = request.form['search_term']
        if term == "":
            flash("Search field empty")
            return redirect('/')
        items = Item
        results = db.session.query(items).filter(
            or_(items.title.contains(term), items.content.contains(term), items.color.contains(term),
                items.size.contains(term))).all()
        # results = Student.query.filter(Student.email.contains(term)).all()
        if not results:
            flash("No matching items.")
            return redirect('/')
        return render_template('search_results.html', results=results)
    else:
        return redirect(url_for('main.index'))


@bp_main.route('/delete_cookie')
def delete_cookie():
    response = make_response(redirect(url_for('main.index')))
    response.set_cookie('name', '', expires=datetime.now())
    return response


@bp_main.route("/item/create", methods=['GET', 'POST'])
@login_required
def new_item():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(title=form.title.data, content=form.content.data, color=form.color.data, size=form.size.data,
                    price=form.price.data, author=current_user)
        db.session.add(item)
        db.session.commit()
        flash('Your item has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_item.html', title='New Item',
                           form=form, legend='New Item')


@bp_main.route("/item/<int:item_id>")
def item(item_id):
    item = Item.query.get_or_404(item_id)
    return render_template('item.html', title=item.title, item=item)


@bp_main.route("/item/<int:item_id>/update", methods=['GET', 'POST'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        abort(403)
    form = ItemForm()
    if form.validate_on_submit():
        item.title = form.title.data
        item.content = form.content.data
        item.size = form.size.data
        item.color = form.color.data
        item.price = form.price.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('main.item', item_id=item.id))
    elif request.method == 'GET':
        form.title.data = item.title
        form.content.data = item.content
        form.color.data = item.color
        form.size.data = item.size
        form.price.data = item.price
    return render_template('create_item.html', title='Update Item',
                           form=form, legend='Update Item')


@bp_main.route("/item/<int:item_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash('Your item has been deleted!', 'success')
    return redirect(url_for('main.home'))
