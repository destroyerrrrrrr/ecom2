import base64
import io
from flask import request, render_template, redirect, url_for, flash, send_from_directory
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, SubmitField, SelectField, DecimalField, FileField
from wtforms.validators import InputRequired, DataRequired, Length
from werkzeug.utils import secure_filename
from ecom.models import Items
from ecom import app
from sqlalchemy import desc
from ecom import db
import datetime
import os
from secrets import token_hex


class AddItemForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Input is required !"), DataRequired("Data is required")])
    price = DecimalField("Price", validators=[InputRequired("Input is required !"), DataRequired("Data is required")])
    category = SelectField(u"Category", choices=[('EL', "Electronics"), ('FD', 'Food'), ('GL', 'Groceries')])
    sub_category = SelectField("Sub-Category", choices=[('AP', 'APPLE'), ('BN', 'BANANA'), ('PS-5', 'PLAY STATION 5')])
    description = TextAreaField("Description",
                                validators=[InputRequired("Input is required !"), DataRequired("Data is required")])
    image = FileField("Image", validators=[FileRequired(), FileAllowed(app.config['ALLOWED_IMAGE_EXTENSIONS'], "Images Only")])
    submit = SubmitField("Submit")


class DeleteItemForm(FlaskForm):
    submit = SubmitField("Delete Item")


class EditItemForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired("Input is required !"), DataRequired("Data is required")])
    price = DecimalField("Price", validators=[InputRequired("Input is required !"), DataRequired("Data is required")])
    description = StringField("Description",
                                validators=[InputRequired("Input is required !"), DataRequired("Data is required")])
    submit = SubmitField("Update")


class FilterForm(FlaskForm):
    title = StringField("Title", validators=[Length(max=20)])
    price = SelectField("Price", coerce=int, choices=[(0, 'Filter By price'), (1, 'Max to Min'), (2, 'Min to Max')])
    submit = SubmitField("Filter")


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/home", methods=['GET', 'POST'])
def home():
    items = Items.query.order_by(desc("id"))
    form = FilterForm(request.args, meta={"csrf": False})

    if form.validate():
        if form.price.data:
            if form.price.data == 1:
                items = Items.query.order_by(desc("price"))
            else:
                items = Items.query.order_by("price")
    else:
        pass
    return render_template("home.html", items=items, form=form)


@app.route("/item/<id>", methods=['GET', 'POST'])
def item(id):
    item = Items.query.get(id)
    if item:
        deleteItemForm = DeleteItemForm()

        return render_template("item.html", item=item, deleteItemForm=deleteItemForm)
    return redirect(url_for("home"))


@app.route("/uploads/<filename>")
def uploads(filename):
    return send_from_directory(app.config["IMAGE_UPLOADS"], filename)


@app.route("/item/<int:id>/delete", methods=["POST"])
def delete_item(id):
    item = Items.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash("Item {} has been successfully deleted".format(item.title), "success")
    else:
        flash("This Item does not exist", "danger")
    return redirect(url_for("home", item=item))


@app.route("/item/<int:id>/edit", methods=["GET", "POST"])
def edit_item(id):
    item = Items.query.filter_by(id=id).first()
    if item:
        form = EditItemForm()
        if form.validate_on_submit():

            form.populate_obj(item)
            db.session.commit()
            flash("Item {} has been sucessfully updated".format(form.title.data), "success")
            return redirect(url_for("item", id=id, item=item))
        if form.errors:
            flash("{}".format(form.errors), "danger")

        return render_template("edit_item.html", item=item, form=form)

    return redirect(url_for('home'))


@app.route("/add/item", methods=["GET", "POST"])
def additem():
    form = AddItemForm()
    if form.validate_on_submit() and form.image.validate(form, extra_validators=(FileRequired(),)):

        filename = save_image_upload(form.image)

        title = form.title.data
        price = form.price.data
        form.category = dict(form.category.choices).get(form.category.data)
        sub_category = dict(form.sub_category.choices).get(form.sub_category.data)
        description = form.description.data
        image = filename
        items = Items(title=title, price=price, category=form.category, sub_category=sub_category,
                      description=description, img=image)
        db.session.add(items)
        db.session.commit()
        flash("Items {} has been sucessfully submitted".format(request.form.get("title")), 'success')
        return redirect(url_for("home"))
    if form.errors:
        flash("{}".format(form.errors), "danger")
    else:
        return render_template("add_item.html", form=form)


def save_image_upload(image):
    format = "%Y%m%dT%H%M%S"
    now = datetime.datetime.utcnow().strftime(format)
    random_string = token_hex(2)
    filename = random_string + "_" + now + "_" + image.data.filename
    filename = secure_filename(filename)
    image.data.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
    return filename




