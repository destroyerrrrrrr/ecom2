from ecom import db


# Creating the models
class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    category = db.Column(db.String(150), nullable=False)
    sub_category = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    img = db.Column(db.String(300))