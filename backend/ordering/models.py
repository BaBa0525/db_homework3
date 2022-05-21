from ordering import db

class User(db.Model):
    __tablename__ = 'users'
    realname = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default="user", nullable=False)
    account = db.Column(db.String(255), primary_key=True)
    phone = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(73), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    balance = db.Column(db.Integer, nullable=False, default=0)
    shopname = db.Column(db.String(255), db.ForeignKey('shops.shopname'), unique=True)
    shop = db.relationship("Shop", backref=db.backref("users", uselist=False))

    def __init__(self, realname, account, phone, password, latitude, longitude):
        self.realname = realname
        self.account = account
        self.phone = phone
        self.password = password
        self.latitude = latitude
        self.longitude = longitude 


class Shop(db.Model):
    __tablename__ = 'shops'
    shopname = db.Column(db.String(255), primary_key=True)
    category = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    def __init__(self, shopname, category, latitude, longitude):
        self.shopname = shopname
        self.category = category
        self.latitude = latitude
        self.longitude = longitude


class Meal(db.Model):
    __tablename__ = 'meals'
    name = db.Column(db.String(255), primary_key=True)
    shopname = db.Column(db.String(255), db.ForeignKey('shops.shopname'), primary_key=True)
    image = db.Column(db.TEXT, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    shop = db.relationship("Shop")

    def __init__(self, name, shopname, image, price, quantity):
        self.name = name
        self.shopname = shopname
        self.image = image
        self.price = price
        self.quantity = quantity

