from flask import request
from datetime import datetime

from ordering import app, db
from ordering.models import *
from ordering.schema import MealSchema

mealSchema = MealSchema()
mealListSchema = MealSchema(many=True)


@app.route('/addmeal', methods=['POST'])
def addMealByShop():
    mealname = request.json['mealname']
    price = request.json['price']
    quantity = request.json['quantity']
    shopname = request.json['shopname']
    image = request.json['image']

    mealData = Meal(mealname, shopname, image, price, quantity)
    db.session.add(mealData)
    db.session.commit()
    return mealSchema.jsonify(mealData)
  


@app.route('/getmeal/<shopname>', methods=['GET'])
def getMealByShopname(shopname):
    mealData = Meal.query.filter_by(shopname=shopname).all()
    return mealListSchema.jsonify(mealData)


@app.route('/deletemeal', methods=['POST'])
def deleteMealFromShop():
    shopname = request.json['shopname']
    mealname = request.json['mealname']

    orderDetailList = OrderDetail.query.filter_by(shopname=shopname, mealname=mealname).all()
    db.session.commit()

    # cancelOrderByIDList([detail.OID for detail in orderDetailList])
    with db.session.begin():
        for orderID in [detail.OID for detail in orderDetailList]:
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

            orderData.update({ 'status': 'Cancelled', 'endTime': datetime.now()})
            transactions.delete()

    mealData = Meal.query.filter_by(shopname=shopname, name=mealname)
    mealData.delete()

    db.session.commit()
    return mealSchema.jsonify(mealData)


@app.route('/editmeal', methods=['PATCH'])
def editMealProperties():
    shopname = request.json['shopname']
    mealname = request.json['mealname']
    price = request.json['price']
    quantity = request.json['quantity']
    
    mealData = Meal.query.filter_by(shopname=shopname, name=mealname)
    mealData.update({'price': price, 'quantity': quantity})

    db.session.commit()
    return mealSchema.jsonify(mealData)
