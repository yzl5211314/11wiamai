from flask import Blueprint
from . import user,member,food,cart,address,order


def createBluePrint():
    bp = Blueprint('v1', __name__)
    user.api.register(bp)
    member.api.register(bp)
    food.api.register(bp)
    cart.api.register(bp)
    address.api.register(bp)
    order.api.register(bp)
    return bp
