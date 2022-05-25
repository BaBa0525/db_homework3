from flask import request
from sqlalchemy import func
from http.client import BAD_REQUEST

from ordering import app, db
from ordering.models import User, Shop, Meal
from ordering.schema import shopSchema, shopListSchema

@app.route('/getshop', methods=['POST'])
def searchShopByFilters():
    shopname = request.json["shopname"]
    distance = request.json["distance"]
    pricelow = request.json["pricelow"]
    pricehigh = request.json["pricehigh"]
    meal = request.json["meal"]
    category = request.json["category"]
    longitude = request.json["longitude"]
    latitude = request.json["latitude"]
    orderingBy = request.json["order"]
    page = int(request.json["page"])

    FILTER_PRICEHIGH = 2
    FILTER_PRICELOW = 1

    condition = (FILTER_PRICEHIGH if pricehigh else 0) | (FILTER_PRICELOW if pricelow else 0)
    pattern = f'%{ meal }%' 

    if condition == (FILTER_PRICEHIGH | FILTER_PRICELOW):
        '''
        filtered: (meal?) pricelow + pricehigh
        '''
        subQuery = Meal.query.filter(
                        Meal.price >= pricelow, 
                        Meal.price <= pricehigh
                    ).with_entities(Shop.shopname).distinct()
    elif condition == FILTER_PRICEHIGH:
        '''
        filtered: (meal?) pricehigh
        '''
        subQuery = Meal.query.filter(
                        Meal.price <= pricehigh, 
                        Meal.name.ilike(pattern)
                    ).with_entities(Shop.shopname).distinct()
    elif condition == FILTER_PRICELOW:
        '''
        filtered: (meal?) pricelow
        '''
        subQuery = Meal.query.filter(
                        Meal.price >= pricelow, 
                        Meal.name.ilike(pattern)
                    ).with_entities(Meal.shopname).distinct()
    elif meal:
        '''
        filtered: meal
        '''
        subQuery = Meal.query.filter(
                        Meal.name.ilike(pattern)
                    ).with_entities(Meal.shopname).distinct()
    else:
        '''
        filtered: nothing
        '''
        subQuery = Shop.query.with_entities(Shop.shopname)

    if distance:
        if distance == 'near':
            lower_bound, upper_bound = -1, 1
        elif distance == 'middle':
            lower_bound, upper_bound = 1, 3
        else:
            lower_bound, upper_bound = 3, 8

        subQuery = Shop.query.filter(
                        Shop.shopname.in_(subQuery),
                        func.distance(latitude, longitude, Shop.latitude, Shop.longitude) > lower_bound,
                        func.distance(latitude, longitude, Shop.latitude, Shop.longitude) <= upper_bound
                    ).with_entities(Shop.shopname).distinct()

    shopListData =  Shop.query.filter(
                        Shop.shopname.ilike(f'%{ shopname }%'), 
                        Shop.category.ilike(f'%{ category }%'),
                        Shop.shopname.in_(subQuery),
                        func.distance(latitude, longitude, Shop.latitude, Shop.longitude) <= 8
                    ).with_entities(Shop.shopname)

    if orderingBy:

        field, direction = orderingBy.split('$')

        if field == 'shopname':
            if direction == 'asc':
                result = Shop.query.filter(
                            Shop.shopname.in_(shopListData)
                        ).order_by(Shop.shopname.asc())
            else:
                result = Shop.query.filter(
                            Shop.shopname.in_(shopListData)
                        ).order_by(Shop.shopname.desc())
        elif field == 'category':
            if direction == 'asc':
                result = Shop.query.filter(
                            Shop.shopname.in_(shopListData)
                        ).order_by(Shop.category.asc())
            else:
                result = Shop.query.filter(
                            Shop.shopname.in_(shopListData)
                        ).order_by(Shop.category.desc())
        else:
            if direction == 'asc':
                result = Shop.query.filter(
                            Shop.shopname.in_(shopListData)
                        ).order_by(func.distance(latitude, longitude, Shop.latitude, Shop.longitude).asc())
            else:
                result = Shop.query.filter(
                            Shop.shopname.in_(shopListData)
                        ).order_by(func.distance(latitude, longitude, Shop.latitude, Shop.longitude).desc())
    else:
        result = Shop.query.filter(Shop.shopname.in_(shopListData))

    shopCount = result.count()
    shopData = result.offset(5 * (page-1)).limit(5).all()

    return { "shops": shopListSchema.dump(shopData), 'count': shopCount }


@app.route('/addshop', methods=['POST'])
def shopRegister():
    account = request.json["account"]
    shopname = request.json["shopname"]
    category = request.json["category"]
    latitude = request.json["latitude"]
    longitude = request.json["longitude"]
    
    if Shop.query.get(shopname) is None:
        shopData = Shop(shopname, category, latitude, longitude)
        db.session.add(shopData)
        User.query.filter(User.account == account).update({'role': "owner", 'shopname': shopname})
        db.session.commit()
        return shopSchema.jsonify(shopData)
    else:
        return ({'message': 'The given data was invalid.', 'error': 'The shopname has been registered.'}, BAD_REQUEST)



@app.route('/getshop/<account>', methods=['GET'])
def getShopFromUser(account):
    userData = User.query.get(account)

    if userData is None or userData.role == 'user':
        return ({'message': 'The given data was invalid.', 'error': 'The user is not owner yet.'}, BAD_REQUEST)

    shopData = Shop.query.get(userData.shopname)
    return shopSchema.jsonify(shopData)


@app.route('/getshopname/<shopname>', methods=['GET'])
def getShopByShopname(shopname):
    shopData = Shop.query.get(shopname)

    if shopData is None: 
        return ({'message': 'The given data was invalid.', 'error': 'The shopname has not been registered.'}, BAD_REQUEST)
    else:
        return shopSchema.jsonify(shopData)
