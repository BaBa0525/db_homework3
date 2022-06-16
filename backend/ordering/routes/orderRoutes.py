from flask import request
from sqlalchemy import func
from http.client import BAD_REQUEST, OK
from datetime import datetime

from ordering import app, db, distance
from ordering.models import *
from ordering.schema import OrderSchema

orderSchema = OrderSchema()
orderListSchema = OrderSchema(many=True)

@app.route('/cancelorder', methods=['POST'])
def cancelOrder():
    orderID = request.json['orderID']
    orderData = Order.query.get(orderID)
    orderData.delete()
    db.session.commit()
    return orderSchema.jsonify(orderData)

@app.route('/getorder/<account>', methods=['GET'])
def getOrder(account):
    orderData = Order.query.filter_by(buyer=account)
    return orderListSchema.jsonify(orderData)


@app.route('/createOrder', methods=['POST'])
def createOrder():
    account = request.json['account']
    shopname = request.json['shopname']
    meals = request.json['meals']
    subtotal = request.json['subtotal']
    deliverFee = request.json['deliverFee']
    method = request.json['type']

    with db.session.begin():
        user = User.query.get(account)
        shop = Shop.query.get(shopname)

        time = datetime.now()

        # create a order
        orderData = Order('Not finished', time, shopname, subtotal, deliverFee, account, method)
        db.session.add(orderData)
        db.session.flush()

        # create all order details and modify other tables
        for meal in meals:
            mealName = meal['name']
            mealPrice = meal['price']
            mealQuantity = meal['orderQuantity']
            mealSubtotal = mealPrice * mealQuantity

            db.session.add(OrderDetail(orderData.OID, shopname, mealName, mealPrice, mealQuantity))
            
            mealData = Meal.query.get((meal['name'], meal['shopname']))
            
            if (modifiedQuantity := mealData.quantity - mealQuantity) < 0:
                db.session.roll_back()
                return ({ 'message': 'The given data was invalid.', 'error': 'Invalid quantity.' }, BAD_REQUEST)

            mealData.update({ 'quantity': modifiedQuantity})

            if (modifiedUserBalance := user.balance - mealSubtotal) < 0:
                db.session.roll_back()
                return ({ 'message': 'The given data was invalid.', 'error': 'Not enough balance.' }, BAD_REQUEST)

            user.update({ 'balance': modifiedUserBalance })

            owner = User.query.filter_by(shopname=shopname).first()
            owner.update({ 'balance': owner + mealSubtotal })

        userTransaction = Transaction(user.account, shopname, 'Payment', time, subtotal + deliverFee)
        ownerTransaction = Transaction(owner.account, user.account, 'Receive', time, subtotal + deliverFee)
        db.session.add_all([userTransaction, ownerTransaction])
    
    return ({ 'message': 'done' }, OK)

        




        
