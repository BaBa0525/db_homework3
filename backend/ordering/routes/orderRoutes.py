from flask import request, jsonify
from http.client import BAD_REQUEST, OK
from datetime import datetime

from ordering import app, db
from ordering.models import *
from ordering.schema import OrderDetailSchema, OrderSchema

orderSchema = OrderSchema()
orderListSchema = OrderSchema(many=True)
orderDetailSchema = OrderDetailSchema()

@app.route('/cancelorder', methods=['POST'])
def cancelOrder():
    orderID = request.json['orderID']

    with db.session.begin():
        orderData = Order.query.filter_by(OID=orderID)
        orderDetails = OrderDetail.query.filter_by(OID=orderID)
        transactions = Transaction.query.filter_by(OID=orderID)

        for detail in orderDetails.all():
            mealQuery = Meal.query.filter_by(shopname=detail.shopname, name=detail.mealname)
            meal = mealQuery.first()
            mealQuery.update({ 'quantity': meal.quantity + detail.quantity })
        
        for transaction in transactions.all():
            userQuery = User.query.filter_by(account=transaction.account)
            user = userQuery.first()
            userQuery.update({ 'balance': user.balance + (-1 * transaction.amount) })

        orderData.delete()
        orderDetails.delete()
        transactions.delete()

    return orderSchema.jsonify(orderData)

@app.route('/getorder/<account>', methods=['GET'])
def getOrder(account):
    orderData = Order.query.filter_by(customer=account)
    return orderListSchema.jsonify(orderData)


@app.route('/getshoporder/<shopname>', methods=['GET'])
def getShopOrder(shopname):
    orderData = Order.query.filter_by(shopname=shopname)
    return orderListSchema.jsonify(orderData)

@app.route('/getorderdetail/<OID>', methods=['GET'])
def getOrderDetail(OID):
    orderDetails = OrderDetail.query.filter_by(OID=OID)

    orderDetailList = orderDetails.all()
    result = [{
            'detail': orderDetailSchema.dump(detail),
            'image': Meal.query.filter_by(shopname=detail.shopname, name=detail.mealname).first().image
        } for detail in orderDetailList]

    return jsonify(result)

@app.route('/addorder', methods=['POST'])
def createOrder():
    account = request.json['account']
    shopname = request.json['shopname']
    meals = request.json['meals']
    subtotal = request.json['subtotal']
    deliverFee = request.json['deliverFee']
    method = request.json['type']

    with db.session.begin():
        userQuery = User.query.filter_by(account=account)
        user = userQuery.first()
        shop = Shop.query.get(shopname)

        time = datetime.now()

        # create a order
        orderData = Order('Not finished', time, shopname, subtotal, deliverFee, account, method)
        db.session.add(orderData)
        db.session.flush()
        print(orderData.OID)
        
        # create all order details and modify other tables
        for meal in meals:
            mealName = meal['name']
            mealPrice = meal['price']
            mealQuantity = meal['orderQuantity']
            mealSubtotal = mealPrice * mealQuantity

            Detail = OrderDetail(orderData.OID, shopname, mealName, mealPrice, mealQuantity)
            print(Detail)
            db.session.add(Detail)

            mealData = Meal.query.filter_by(name=mealName, shopname=shopname)
            
            if (modifiedQuantity := mealData.first().quantity - mealQuantity) < 0:
                db.session.rollback()
                return ({ 'message': 'Not enough meal quantity.' }, BAD_REQUEST)

            mealData.update({ 'quantity': modifiedQuantity })


            if (modifiedUserBalance := user.balance - mealSubtotal) < 0:
                db.session.rollback()
                return ({ 'message': 'Not enough balance.' }, BAD_REQUEST)

            userQuery.update({ 'balance': modifiedUserBalance })

            print("ya")
            ownerQuery = User.query.filter_by(shopname=shopname)
            owner = ownerQuery.first()
            ownerQuery.update({ 'balance': owner.balance + mealSubtotal })

        userTransaction = Transaction(orderData.OID, user.account, shopname, 'shop', 'Payment', time, -1 * (subtotal + deliverFee))
        ownerTransaction = Transaction(orderData.OID, owner.account, user.account, 'user', 'Receive', time, subtotal + deliverFee)
        db.session.add_all([userTransaction, ownerTransaction])
    
    return ({ 'message': 'done' }, OK)

        




        
