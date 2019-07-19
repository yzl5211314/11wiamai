from app.libs.redprint import RedPrint
from flask import jsonify
from app.models.food import Food,Category
from flask import request
from app.utils.common import buildPicUrl
from app.models.cart import MemberCart

api = RedPrint('food',description='食物')

@api.route('/search')
def search():

    """
    banners: [
                {
                    "id": 1,
                    "pic_url": "/images/food.jpg"
                },
                {
                    "id": 2,
                    "pic_url": "/images/food.jpg"
                },
                {
                    "id": 3,
                    "pic_url": "/images/food.jpg"
                }
            ],
            categories: [
                {id: 0, name: "全部"},
                {id: 1, name: "川菜"},
                {id: 2, name: "东北菜"},
            ],
    :return:
    """
    res = {'code':1,'msg':'成功','data':{}}

    categories = []
    categories.append({'id':0,'name':'全部'})
    #根据状态和权重查分类
    all_category = Category.query.filter_by(status=1).order_by(Category.weight.desc()).all()
    for category in all_category:
        temp_data = {}
        temp_data['id'] = category.id
        temp_data['name'] = category.name
        categories.append(temp_data)

    banners = []
    foods = Food.query.filter_by(status=1).order_by(Food.month_count.desc()).limit(3).all()
    for food in foods:
        temp_data = {}
        temp_data['id'] = food.id
        temp_data['pic_url'] = buildPicUrl(food.main_image)
        banners.append(temp_data)
    #创建数据
    res['data']['categories'] = categories
    res['data']['banners'] = banners
    return jsonify(res)

"""
                {
                    "id": 1,
                    "name": "小鸡炖蘑菇-1",
                    "min_price": "15.00",
                    "price": "15.00",
                    "pic_url": "/images/food.jpg"
                },
"""
import time
@api.route('/all')
def all():
    res = {'code': 1, 'msg': '成功', 'data': {}}
    try:

        cid = request.args.get('cid')
        page = request.args.get('page')

        #如果没传id 就设置这个
        if not cid:
            cid = '0'

        if not page:
            page = '1'
        #如果传字符串就设置这个
        cid = int(cid)
        page = int(page)

        """
        每页1个
        """
        pagesize = 1
        # offset偏移量公式
        offset = (page-1)*pagesize

        goods = []

        query = Food.query.filter_by(status=1)

        if cid == 0:
            foods = query.offset(offset).limit(pagesize).all()
        else:
            foods = query.filter_by(cat_id=cid).offset(offset).limit(pagesize).all()


        for food in foods:
            temp_food = {}
            temp_food['id'] = food.id
            temp_food['name'] = food.name
            temp_food['min_price'] = str(food.price)
            temp_food['price'] = str(food.price)
            temp_food['pic_url'] = buildPicUrl(food.main_image)
            goods.append(temp_food)

        res['data']['goods'] = goods

        #是否还有数据
        if len(foods) < pagesize:
            res['data']['ismore'] = 0
        else:
            res['data']['ismore'] = 1

        # time.sleep(10)


        return jsonify(res)
    except Exception as e:
        res['code'] = -1
        res['msg'] = '参数错误'
        return jsonify(res)

@api.route('/info')
def info():
    res = {'code':1,'msg':'成功','data':{}}
    try:
        id = request.args.get('id')
        if not id:
            res['code'] = -1
            res['msg'] = '参数不能为空'
            return jsonify(res)
        id = int(id)
        if id <= 0:
            res['code'] = -1
            res['msg'] = '参数有误'
            return jsonify(res)
        # """
        # "info": {
        #             "id": 1,
        #             "name": "小鸡炖蘑菇",
        #             "summary": '<p>多色可选的马甲</p><p><img src="http://www.timeface.cn/uploads/times/2015/07/071031_f5Viwp.jpg"/></p><p><br/>相当好吃了</p>',
        #             "total_count": 2,
        #             "comment_count": 2,
        #             "stock": 2,
        #             "price": "80.00",
        #             "main_image": "/images/food.jpg",
        #             "pics": ['/images/food.jpg', '/images/food.jpg']
        #         },
        # """
        food = Food.query.get(id)
        info = {}
        info['id'] = food.id
        info['name'] = food.name
        info['summary'] = food.summary
        info['total_count'] = food.total_count
        info['comment_count'] = food.comment_count
        info['stock'] = food.stock
        info['price'] = str(food.price)
        info['main_image'] = buildPicUrl(food.main_image)
        info['pics'] = [buildPicUrl(food.main_image),buildPicUrl(food.main_image),buildPicUrl(food.main_image)]
        res['data']['info'] = info
        # """
        # 一个商品对应多个图片  图片表
        # 以空间换时间
        # """
        return jsonify(res)
    except Exception as e:
        res['code'] = -1
        res['msg'] = '参数错误'
        return jsonify(res)