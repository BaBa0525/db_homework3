from flask import request
from http.client import BAD_REQUEST
from datetime import datetime

from ordering import app, db
from ordering.models import User, Transaction
from ordering.schema import UserSchema, TransactionSchema
from ordering.routes import generateSalt, getHashed


ERROR_USER_NOT_EXISTS =  ({ 'message': 'The given data was invalid.', 'error': 'The user does not exists.' }, BAD_REQUEST)
userSchema = UserSchema()
transactionListSchema = TransactionSchema(many=True)


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


@app.route('/getuser/<account>', methods = ['GET'])
def getUserData(account):
    if (userData := User.query.get(account)) is None:
        return ERROR_USER_NOT_EXISTS
    else:
        return userSchema.jsonify(userData)


@app.route('/check/', methods = ['GET'])
def checkAccountExistence_NoArg():
    return { 'exists': False }
    

@app.route('/check/<account>', methods = ['GET'])
def checkAccountExistence(account):
    if User.query.get(account) is None:
        return { 'exists': False }
    else:
        return { 'exists': True }


@app.route('/location', methods=['PUT'])
def updateLocationOfUser():
    account   = request.json['account']
    latitude  = request.json['latitude']
    longitude = request.json['longitude']

    userData = User.query.filter_by(account=account)
    userData.update({'latitude': latitude, 'longitude': longitude})

    db.session.commit()
    return userSchema.jsonify(userData)


@app.route('/recharge', methods=['PATCH'])
def recharge():
    account = request.json['account']
    value = int(request.json['value'])

    with db.session.begin():
        userData = User.query.filter_by(account=account)
        time = datetime.now()
        user = userData.first()
        userData.update({ 'balance': user.balance + value })
        userTransaction = Transaction(None, user.account, user.account, 'user', 'Recharge', time, value)
        db.session.add(userTransaction)
    
    return userSchema.jsonify(userData)


@app.route('/transaction', methods = ['POST'])
def getTransaction():
    account = request.json['account']
    action = request.json['action']
    print(action, account)

    if action == 'All':
        transaction = Transaction.query.filter(db.or_(Transaction.account==account, Transaction.trader==account))
    else:
        transaction = Transaction.query.filter(db.or_(Transaction.account==account, Transaction.trader==account), Transaction.action==action)

    if transaction is None:
        return ERROR_USER_NOT_EXISTS
    else:
        return transactionListSchema.jsonify(transaction)