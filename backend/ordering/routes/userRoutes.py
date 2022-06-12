from flask import request
from http.client import BAD_REQUEST

from ordering import app, db
from ordering.models import User
from ordering.schema import UserSchema
from ordering.routes import generateSalt, getHashed


ERROR_USER_NOT_EXISTS =  ({ 'message': 'The given data was invalid.', 'error': 'The user does not exists.' }, BAD_REQUEST)
userSchema = UserSchema()


@app.route('/login', methods = ['POST'])
def userLogin():
    account = request.json['account']
    password = request.json['password']

    if (user := User.query.get(account)) is None:
        return ERROR_USER_NOT_EXISTS
    
    salt, password_stored = user.password.split('$')

    password_hashed = getHashed(salt, password)

    if password_hashed == password_stored:
        return userSchema.jsonify(user)
    else:
        return ({ 'message': 'The given data was invalid.', 'error': 'The password was incorrect.' }, BAD_REQUEST)


@app.route('/register', methods = ['POST'])
def userRegister():
    realname = request.json['realname']
    account = request.json['account']
    phone = request.json['phone']
    password = request.json['password']
    latitude = request.json['latitude']
    longitude = request.json['longitude']

    if (userData := User.query.get(account)) is None:
        salt = generateSalt(saltLength=8)
        password_hashed = getHashed(salt, password)

        userData = User(realname, account, phone, f'{salt}${password_hashed}', latitude, longitude)

        db.session.add(userData)
        db.session.commit()
        return userSchema.jsonify(userData)
    else:
        return ({ 'message': 'The given data was invalid.', 'error': 'The account has been registered.' }, BAD_REQUEST)



@app.route('/check/<account>', methods = ['GET'])
def checkAccountExistence(account):
    if User.query.get(account) is None:
        return { 'exists': False}
    else:
        return { 'exists': True }


@app.route('/location', methods=['PUT'])
def updateLocationOfUser():
    account   = request.json['account']
    latitude  = request.json['latitude']
    longitude = request.json['longitude']

    if (userData := User.query.filter_by(account=account)) is None:
        return ERROR_USER_NOT_EXISTS
    
    userData.update({'latitude': latitude, 'longitude': longitude})

    db.session.commit()
    return userSchema.jsonify(userData)
