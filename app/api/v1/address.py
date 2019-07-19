from app.libs.redprint import RedPrint
from app import db
from flask import jsonify,request,g
from app.models.address import MemberAddress



api = RedPrint('address',description='地址模块')
@api.route('/add',methods=['POST'])
def add():
    res = {'code': 1, 'msg': '成功', 'data': {}}

    member = g.member
    if not member:
        res['code'] = -1
        res['msg'] = '用户不存在'
        return jsonify(res)

    nickname =request.form.get('nickname')
    mobile =request.form.get('mobile')
    province_id =request.form.get('province_id')
    province_str =request.form.get('province_str')
    city_id =request.form.get('city_id')
    city_str =request.form.get('city_str')
    area_id =request.form.get('area_id')
    area_str =request.form.get('area_str')
    address =request.form.get('address')

    count = MemberAddress.query.filter_by(is_default = 1).count()

    memberaddress = MemberAddress()
    memberaddress.nickname = nickname
    memberaddress.mobile = mobile
    memberaddress.province_id = province_id
    memberaddress.province_str = province_str
    memberaddress.city_id = city_id
    memberaddress.city_str = city_str
    memberaddress.area_id = area_id
    memberaddress.area_str = area_str
    memberaddress.address = address
    memberaddress.member_id = member.id

    if count == 0:
        memberaddress.is_default = 1
    else:
        memberaddress.is_default = 0

    db.session.add(memberaddress)
    db.session.commit()

    return jsonify(res)
