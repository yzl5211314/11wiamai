from app.libs.redprint import RedPrint
from flask import jsonify,request,g
from app.models.food import Food
from app.models.cart import MemberCart
from app import db
from app.utils.common import buildPicUrl
import json


api = RedPrint('cart',description='购物车')

@api.route('/add',methods=['POST'])
def add():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    try:


        member = g.member
        if not member:
            res['code'] = -1
            res['msg'] = '用户不存在'
            return jsonify(res)


        id = request.form.get('id')#食品id
        num = int(request.form.get('num'))
        fromtype = int(request.form.get('fromtype'))


        food = Food.query.get(id)

        if not food:
            res['code'] = -1
            res['msg'] = '商品不存在'
            return jsonify(res)


        if food.status != 1:
            res['code'] = -1
            res['msg'] = '商品已下架'
            return jsonify(res)

        if fromtype == 0:
            if num < 1:
                res['code'] = -1
                res['msg'] = '商品数量不对'
                return jsonify(res)
        else:
            if num != 1 and num != -1:
                res['code'] = -1
                res['msg'] = '商品数量不对2'
                return jsonify(res)

        if num > food.stock:
            res['code'] = -1
            res['msg'] = '库存不足'
            return jsonify(res)

        membercart = MemberCart.query.filter_by(member_id=member.id, food_id=id).first()

        if not membercart:
            membercart = MemberCart()
            membercart.food_id = id
            membercart.member_id = member.id
            membercart.quantity = num
        else:
            membercart.quantity = membercart.quantity + num

        db.session.add(membercart)
        db.session.commit()


        return jsonify(res)
    except Exception as e:
        res['code'] = -1
        res['msg'] = '参数错误'
        return jsonify(res)

@api.route('/list')
def list():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)

    membercarts = MemberCart.query.filter_by(member_id=member.id).all()

    list = []
    totalPrice = 0
    for cart in membercarts:
        temp_food = {}
        food = Food.query.get(cart.food_id)
        if not food:
            continue
        if food.status != 1:
            continue
        temp_food['id'] = cart.id
        temp_food['food_id'] = food.id
        temp_food['pic_url'] = buildPicUrl(food.main_image)
        temp_food['name'] = food.name
        temp_food['price'] = str(food.price)
        temp_food['active'] = 'true'
        temp_food['number'] = cart.quantity

        list.append(temp_food)
        totalPrice += cart.quantity * food.price

    res['data']['list'] = list
    res['data']['totalPrice'] = str(totalPrice)


    return jsonify(res)


@api.route('/delete',methods=['POST'])
def delete():
    res = {'code':1,'msg':'成功','data':{}}
    ids = request.form.get('ids')
    # member = g.member
    # if not member:
    #     res['code'] = -1
    #     res['msg'] = '用户不存在'
    #     return jsonify(res)

    ids = json.loads(ids)

    for id in ids:
        membercart = MemberCart.query.get(id)
        db.session.delete(membercart)
        db.session.commit()

    return jsonify(res)

