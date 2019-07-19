//获取应用实例
var app = getApp();

Page({
    data: {
        ids: [],
        address_id: 0,
        note:'',
        // goods_list: [
        //     {
        //         id: 22,
        //         name: "小鸡炖蘑菇",
        //         price: "85.00",
        //         pic_url: "/images/food.jpg",
        //         number: 1,
        //     },
        //     {
        //         id: 22,
        //         name: "小鸡炖蘑菇",
        //         price: "85.00",
        //         pic_url: "/images/food.jpg",
        //         number: 1,
        //     }
        // // ],
        // default_address: {
        //     name: "编程浪子",
        //     mobile: "12345678901",
        //     detail: "上海市浦东新区XX",
        // },
        // yun_price: "1.00",
        // pay_price: "85.00",
        // total_price: "86.00",
        // params: null
    },
    onShow: function () {
        var that = this;
    },
    onLoad: function (e) {

        var that = this;
        that.setData({
            ids: JSON.parse(e.ids),

        })
        that.getOrderIndex()

    },
    getInput:function (e) {
        this.setData({
            note:e.detail.value
        })
    },
    createOrder: function (e) {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/create'),
            method: 'POST',
            data: {
                'ids': JSON.stringify(that.data.ids),
                'address_id': that.data.address_id,
                'note': that.data.note
            },
            header: app.getRequestHeader(),
            success(res) {
                console.log(res.data)
                if (res.data.code == -1) {
                    app.alert({
                        'content': res.data.msg
                    })
                    return
                }
            }
        })
        // wx.showLoading();

        // },
        //
        wx.redirectTo({
            url: "/pages/my/order_list"
        });
    },
    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    }
    ,
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },
    getOrderIndex: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/index'),
            method: 'POST',
            data: {
                'ids': JSON.stringify(that.data.ids),

            },
            header: app.getRequestHeader(),
            success(res) {
                console.log(res.data)
                if (res.data.code == -1) {
                    app.alert({
                        'content': res.data.msg
                    });
                    return
                }
                that.setData({
                    goods_list: res.data.data.goods_list,
                    default_address: res.data.data.default_address,
                    pay_price: res.data.data.pay_price,
                    yun_price: res.data.data.yun_price,
                    total_price: res.data.data.total_price,
                    address_id:res.data.data.default_address.id
                })
            }
        })
    }

})
;
