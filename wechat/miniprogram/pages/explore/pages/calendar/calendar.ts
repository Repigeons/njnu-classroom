// calendar.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {

  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(/*options*/) {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow() {

  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {
    return {
      title: '校历查询',
      path: 'pages/calendar/calendar'
      + `?page=calendar`,
      image: 'images/logo.png'
    }
  }
})