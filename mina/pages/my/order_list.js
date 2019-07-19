var app = getApp();
Page({
    data: {
        statusType: ["待付款", "待发货", "待收货", "待评价", "已完成", "已关闭"],
        status: ["-8", "-7", "-6", "-5", "1", "0"],
        currentType: 0,
        tabClass: ["", "", "", "", "", ""]
    },
    statusTap: function (e) {
        var curType = e.currentTarget.dataset.index;
        this.data.currentType = curType;
        this.setData({
            currentType: curType,
        });
        console.log(this.data.status[curType])

        this.onShow();
        this.getOrderList()
    },
    orderDetail: function (e) {
        wx.navigateTo({
            url: "/pages/my/order_info"
        })
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载
        this.getOrderList()
    },
    onReady: function () {
        // 生命周期函数--监听页面初次渲染完
    },
    onShow: function () {
        var that = this;
        // that.setData({
        //     order_list: [
        //         {
        //             status: -8,
        //             status_desc: "待支付",
        //             date: "2018-07-01 22:30:23",
        //             order_number: "20180701223023001",
        //             note: "记得周六发货",
        //             total_price: "85.00",
        //             goods_list: [
        //                 {
        //                     pic_url: "/images/food.jpg"
        //                 },
        //                 {
        //                     pic_url: "/images/food.jpg"
        //                 }
        //             ]
        //         }
        //     ]
        // });
    },
    onHide: function () {
        // 生命周期函数--监听页面隐藏

    },
    onUnload: function () {
        // 生命周期函数--监听页面卸载

    },
    onPullDownRefresh: function () {
        // 页面相关事件处理函数--监听用户下拉动作

    },
    onReachBottom: function () {
        // 页面上拉触底事件的处理函数

    },
    getOrderList: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/list'),
            method: 'GET',
            data:{
                status:that.data.status[that.data.currentType]
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
                    order_list:res.data.data.order_list
                })
            }
        })
    },
    goComment:function () {
        wx.navigateTo({
            url:"/pages/my/comment"
        })

    }
})
