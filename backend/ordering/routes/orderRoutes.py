from flask import request
from sqlalchemy import func
from http.client import BAD_REQUEST

from ordering import app, db
from ordering.models import User, Shop, Meal, Order
from ordering.schema import OrderSchema

orderSchema = OrderSchema()
orderListSchema = OrderSchema(many=True)

@app.route('/cancelorder', methods=['DELETE'])
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

