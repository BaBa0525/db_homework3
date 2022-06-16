from flask import request
from sqlalchemy import func
from http.client import BAD_REQUEST

from ordering import app, db
from ordering.models import User, Shop, Meal
from ordering.schema import ShopSchema


shopSchema = ShopSchema()
shopListSchema = ShopSchema(many=True)


@app.route('/getshop', methods=['POST'])
def searchShopByFilters():
    shopname = request.json['shopname']
    distance = request.json['distance']
    pricelow = request.json['pricelow']
    pricehigh = request.json['pricehigh']
    meal = request.json['meal']
    category = request.json['category']
    longitude = request.json['longitude']
    latitude = request.json['latitude']
    orderingBy = request.json['order']
    page = int(request.json['page'])

    pattern = f'%{ meal }%'

    if pricehigh and pricelow:
        '''
        filtered: (meal?) pricelow + pricehigh
        '''
        subQuery = Meal.query.filter(
                        Meal.price >= pricelow, 
                        Meal.price <= pricehigh,
                        Meal.name.ilike(pattern)
                    ).with_entities(Meal.shopname).distinct()
    elif pricehigh:
        '''
        filtered: (meal?) pricehigh
        '''
        subQuery = Meal.query.filter(
                        Meal.price <= pricehigh, 
                        Meal.name.ilike(pattern)
                    ).with_entities(Meal.shopname).distinct()
    elif pricelow:
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

    if distance is None or distance == '':
        lower_bound, upper_bound = -1, 8000
    if distance == 'near':
        lower_bound, upper_bound = -1, 1000
    elif distance == 'middle':
        lower_bound, upper_bound = 1000, 3000
    elif distance == 'far':
        lower_bound, upper_bound = 3000, 8000

    shopListData =  Shop.query.filter(
                        Shop.shopname.ilike(f'%{ shopname }%'), 
                        Shop.category.ilike(f'%{ category }%'),
                        Shop.shopname.in_(subQuery),
                        func.distance(latitude, longitude, Shop.latitude, Shop.longitude) > lower_bound,
                        func.distance(latitude, longitude, Shop.latitude, Shop.longitude) <= upper_bound
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

    return { 'shops': shopListSchema.dump(shopData), 'count': shopCount }


@app.route('/addshop', methods=['POST'])
def shopRegister():
    account = request.json['account']
    shopname = request.json['shopname']
    category = request.json['category']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    
    if Shop.query.get(shopname) is None:
        shopData = Shop(shopname, category, latitude, longitude)
        db.session.add(shopData)
        User.query.filter_by(account=account).update({'role': 'owner', 'shopname': shopname})
        db.session.commit()
        return shopSchema.jsonify(shopData)
    else:
        return ({'message': 'The given data was invalid.', 'error': 'The shopname has been registered.'}, BAD_REQUEST)


@app.route('/getshop/<shopname>', methods=['GET'])
def getShopByShopname(shopname):
    shopData = Shop.query.get(shopname)

    if shopData is None: 
        return ({'message': 'The given data was invalid.', 'error': 'The shopname has not been registered.'}, BAD_REQUEST)
    else:
        return shopSchema.jsonify(shopData)


@app.route('/checkshop/', methods = ['GET'])
def checkShopExistence_NoArg():
    return { 'exists': False }


@app.route('/checkshop/<shopname>', methods = ['GET'])
def checkShopExistence(shopname):
    if Shop.query.get(shopname) is None:
        return { 'exists': False }
    else:
        return { 'exists': True }
