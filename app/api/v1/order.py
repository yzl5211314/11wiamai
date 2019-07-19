from app.libs.redprint import RedPrint
from app import db
from flask import jsonify, request, g
import json
from app.models.cart import MemberCart
from app.models.food import Food
from app.utils.common import buildPicUrl
from app.models.address import MemberAddress
from app.models.order import PayOrder, PayOrderItem
import hashlib
import time,random



api = RedPrint('order', description='订单模块')


@api.route('/index', methods=['POST'])
def center():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    ids = request.form.get('ids')  # 商品的ids

    ids = json.loads(ids)  # 转成列表

    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)

    yun_price = 0
    pay_price = 0
    goods_list = []
    for id in ids:
        temp_data = {}
        membercart = MemberCart.query.filter_by(food_id=id, member_id=member.id).first()
        food = Food.query.get(id)

        # 可能需要判断商品是否存在和状态
        temp_data['id'] = id
        temp_data['name'] = food.name
        temp_data['price'] = str(food.price)
        temp_data['pic_url'] = buildPicUrl(food.main_image)
        temp_data['number'] = membercart.quantity
        goods_list.append(temp_data)

        pay_price += food.price * membercart.quantity

    # 查询此会员的默认地址
    memberaddress = MemberAddress.query.filter_by(member_id=member.id, is_default=1).first()

    # 地址
    default_address = {}
    default_address['id'] = memberaddress.id
    default_address['name'] = memberaddress.nickname
    default_address['mobile'] = memberaddress.mobile
    default_address['address'] = memberaddress.showAddress()

    total_price = yun_price + pay_price

    res['data']['goods_list'] = goods_list
    res['data']['default_address'] = default_address
    res['data']['total_price'] = str(total_price)
    res['data']['yun_price'] = str(yun_price)
    res['data']['pay_price'] = str(pay_price)

    return jsonify(res)


@api.route('/create', methods=['POST'])
def create():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    try:
        member = g.member
        if not member:
            res['code'] = -1
            res['msg'] = '用户不存在'
            return jsonify(res)

        ids = request.form.get('ids')  # 商品的ids
        address_id = request.form.get('address_id')
        note = request.form.get('note')

        ids = json.loads(ids)


        pay_price = 0
        yun_price = 0
        # 根据ids去查购物车
        for id in ids:
            membercart = MemberCart.query.filter_by(member_id=member.id, food_id=id).first()

            if not membercart:  #是否合适
                continue

            food = Food.query.get(id)  #查食品表
            if not food or food.status != 1:
                continue

            pay_price+=food.price*membercart.quantity

        memberaddress = MemberAddress.query.get(address_id)#查地址

        if not memberaddress:
            res['code'] = -1
            res['msg'] = '地址不存在'
            return jsonify(res)


        # 生成订单
        payorder = PayOrder()
        payorder.order_sn = geneOrderSn()
        payorder.total_price = yun_price+pay_price
        payorder.yun_price = yun_price
        payorder.pay_price = pay_price
        payorder.note = note
        payorder.status = -8  #待支付
        payorder.express_status = -1  #待发货
        payorder.express_address_id = address_id
        payorder.express_info = memberaddress.showAddress()
        payorder.comment_status = -1 #待评论
        payorder.member_id = member.id

        db.session.add(payorder)

        #扣库存
        foods = db.session.query(Food).filter(Food.id.in_(ids)).with_for_update().all()
        temp_stock = {}  #临时的库存

        for food in foods:
            temp_stock[food.id] = food.stock
        # time.sleep(15)


        for id in ids:
            membercart = MemberCart.query.filter_by(member_id=member.id, food_id=id).first()

            if not membercart:
                res['code'] = -1
                res['msg'] = '购物车不存在'
                return jsonify(res)

            if membercart.quantity > temp_stock[id]:
                res['code'] = -1
                res['msg'] = '库存不足'
                return jsonify(res)
            food = db.session.query(Food).filter(Food.id==id).update({
                'stock':temp_stock[id]-membercart.quantity
            })



            if not food:
                raise Exception('更新失败')
            food = Food.query.get(id)  #查表

            # 生成订单的商品从表
            payorderitem = PayOrderItem()

            payorderitem.quantity = membercart.quantity
            payorderitem.price = food.price
            payorderitem.note = note
            payorderitem.status = 1
            payorderitem.pay_order_id = payorder.id
            payorderitem.member_id = member.id
            payorderitem.food_id = id

            db.session.add(payorderitem)

            #清空购物车已经下单的商品

            db.session.delete(membercart)  #删除已经下单的购物车

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        res['code'] = -1
        res['msg'] = '出现异常'
        return jsonify(res)


    return jsonify(res)




def geneOrderSn():
    m = hashlib.md5()
    sn = None
    while True:
        str = "%s-%s" % (int(round(time.time() * 1000)), random.randint(0, 9999999))
        m.update(str.encode("utf-8"))
        sn = m.hexdigest()
        if not PayOrder.query.filter_by(order_sn=sn).first():
            break
    return sn
@api.route('/list')

def list():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    status = request.args.get('status')
    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)
    order_list = []
    payorders = PayOrder.query.filter_by(member_id=member.id,status=status).all()
    for payorder in payorders:
        temp_data = {}
        temp_data['status'] = payorder.status
        temp_data['status_desc'] = payorder.status_desc
        temp_data['date'] = payorder.create_time.strftime('%Y-%m-%d %H:%M:%S')
        temp_data['note'] = payorder.note
        temp_data['total_price'] =str(payorder.total_price)
        temp_data['order_number'] = payorder.create_time.strftime('%Y%m%d%H%M%S')+str(payorder.id).zfill(5)
        goods_list =[]
        payorderitems = PayOrderItem.query.filter_by(pay_order_id=payorder.id).all()
        for payorderitme in payorderitems:
            food = Food.query.get(payorderitme.food_id)
            temp_food = {}
            temp_food['pic_url'] = buildPicUrl(food.main_image)
            goods_list.append(temp_food)
        temp_data['goods_list'] = goods_list
        order_list.append(temp_data)
    res['data']['order_list'] = order_list
    return jsonify(res)


