from flask import request

from ordering import app, db
from ordering.models import Meal
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


@app.route('/deletemeal', methods=['DELETE'])
def deleteMealFromShop():
    shopname = request.json['shopname']
    mealname = request.json['mealname']

    mealData = Meal.query.filter_by(shopname=shopname, name=mealname)
    mealData.delete()

    db.session.commit()
    return mealSchema.jsonify(mealData)


@app.route('/editmeal', methods=['PUT'])
def editMealProperties():
    shopname = request.json['shopname']
    mealname = request.json['mealname']
    price = request.json['price']
    quantity = request.json['quantity']
    
    mealData = Meal.query.filter_by(shopname=shopname, name=mealname)
    mealData.update({'price': price, 'quantity': quantity})

    db.session.commit()
    return mealSchema.jsonify(mealData)
