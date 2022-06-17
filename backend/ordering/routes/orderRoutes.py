from flask import request, jsonify
from http.client import BAD_REQUEST, OK
from datetime import datetime

from ordering import app, db
from ordering.models import *
from ordering.schema import OrderDetailSchema, OrderSchema

orderSchema = OrderSchema()
orderListSchema = OrderSchema(many=True)
orderDetailSchema = OrderDetailSchema()
orderDetailListSchema = OrderDetailSchema(many=True)


@app.route('/cancelorder', methods=['POST'])
def cancelOrder():
    orderIDList = request.json['orderIDs']
   
    # orderData = cancelOrderByIDList(orderIDList)
    with db.session.begin():
        time = datetime.now()

        for orderID in orderIDList:
            orderData = Order.query.filter_by(OID=orderID)
            orderDetails = OrderDetail.query.filter_by(OID=orderID)
            transactions = Transaction.query.filter_by(OID=orderID)

            order = orderData.first()
            if order.status == 'Finished':
                db.session.rollback()
                return ({ 'message': 'The orders could not be cancelled. (status: Finished)' }, BAD_REQUEST)
            elif order.status == 'Cancelled':
                db.session.rollback()
                return ({ 'message': 'The orders could not be cancelled. (status: Cancelled)' }, BAD_REQUEST)

            for detail in orderDetails.all():
                mealQuery = Meal.query.filter_by(shopname=detail.shopname, name=detail.mealname)
                meal = mealQuery.first()
                mealQuery.update({ 'quantity': meal.quantity + detail.quantity })
            
            for transaction in transactions.all():
                userQuery = User.query.filter_by(account=transaction.account)
                user = userQuery.first()
                userQuery.update({ 'balance': user.balance + (-1 * transaction.amount) })

                action = 'Receive' if transaction.action == 'Payment' else 'Payment'
                newTransaction = Transaction(None, transaction.account, transaction.trader, transaction.traderRole, action, time, -1 * transaction.amount)
                db.session.add(newTransaction)

            orderData.update({ 'status': 'Cancelled', 'endTime': datetime.now()})

    return orderSchema.jsonify(orderData)


@app.route('/getorder', methods=['POST'])
def getOrder():
    account = request.json['account']
    status = request.json['status']
    
    if status == 'All' :
        orderStatus = ['Finished', 'Not finished', 'Cancelled']
    else:
        orderStatus = [status]
    orderData = Order.query.filter(Order.status.in_(orderStatus),Order.customer==account)
    return orderListSchema.jsonify(orderData)


@app.route('/getshoporder', methods=['POST'])
def getShopOrder():
    shopname = request.json['shopname']
    status = request.json['status']
    if status == 'All' :
        orderStatus = ['Finished', 'Not finished', 'Cancelled']
    else: 
        orderStatus = [status]
    orderData = Order.query.filter(Order.status.in_(orderStatus),Order.shopname==shopname)
    return orderListSchema.jsonify(orderData)


@app.route('/getorderdetail/<OID>', methods=['GET'])
def getOrderDetail(OID):
    orderDetails = OrderDetail.query.filter_by(OID=OID)

    orderDetailList = orderDetails.all()

    return orderDetailListSchema.jsonify(orderDetailList)


@app.route('/addorder', methods=['POST'])
def createOrder():
    account = request.json['account']
    shopname = request.json['shopname']
    meals = request.json['meals']
    subtotal = request.json['subtotal']
    deliverFee = request.json['deliverFee']
    method = request.json['type']
    totalCost = subtotal + deliverFee

    with db.session.begin():
        userQuery = User.query.filter_by(account=account)
        user = userQuery.first()
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
            mealPicture = meal['image']

            Detail = OrderDetail(orderData.OID, shopname, mealName, mealPicture, mealPrice, mealQuantity)
            db.session.add(Detail)

            mealData = Meal.query.filter_by(name=mealName, shopname=shopname)

            if mealData.first() is None:
                db.session.rollback()
                return ({ 'message': 'Meal not exist.' }, BAD_REQUEST)

            if (modifiedQuantity := mealData.first().quantity - mealQuantity) < 0:
                db.session.rollback()
                return ({ 'message': 'Not enough meal quantity.' }, BAD_REQUEST)

            mealData.update({ 'quantity': modifiedQuantity })

        if (modifiedUserBalance := user.balance - totalCost) < 0:
            db.session.rollback()
            return ({ 'message': 'Not enough balance.' }, BAD_REQUEST)

        userQuery.update({ 'balance': modifiedUserBalance })

        ownerQuery = User.query.filter_by(shopname=shopname)
        owner = ownerQuery.first()
        ownerQuery.update({ 'balance': owner.balance + totalCost })

        '''
        1. customer pay to shop
        2. owner receive from customer
        '''
        userTransaction = Transaction(orderData.OID, user.account, shopname, 'shop', 'Payment', time, -1 * totalCost)
        ownerTransaction = Transaction(orderData.OID, owner.account, user.account, 'user', 'Receive', time, totalCost)
        db.session.add_all([userTransaction, ownerTransaction])
    
    return ({ 'message': 'done' }, OK)

        
@app.route('/finishorder', methods=['POST'])
def finishOrder():
    orderIDList = request.json['orderIDs']

    # orderQuery = finishOrderByIDList(orderIDList)
    with db.session.begin():
        for orderID in orderIDList:
            orderQuery = Order.query.filter_by(OID=orderID)

            order = orderQuery.first()
            if order.status == 'Finished':
                db.session.rollback()
                return ({ 'message': 'The orders could not be finished. (status: Finished)' }, BAD_REQUEST)
            elif order.status == 'Cancelled':
                db.session.rollback()
                return ({ 'message': 'The orders could not be cancelled. (status: Cancelled)' }, BAD_REQUEST)

            orderQuery.update({ 'status': 'Finished', 'endTime': datetime.now() })

    return orderSchema.jsonify(orderQuery)
        
