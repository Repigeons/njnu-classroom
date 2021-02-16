// explore.ts
// 获取应用实例
// const app = getApp<IAppOption>()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    fullYear: new Date().getFullYear(),
    grids: [
      {
        "url": "pages/searchmore/searchmore",
        "text": "更多搜索"
      },
      {
        "url": "pages/shuttle/shuttle",
        "text": "校内班车时刻表"
      },
      {
        "url": "pages/calendar/calendar",
        "text": "校历"
      },
      {
        "url": ".",
        "text": "定制时间表"
      },
      {
        "url": ".",
        "text": "一键支持"
      },
      {
        "target": "miniProgram",
        "text": "反馈",
        "appId": "*",
        "bindfail": () => {console.log("feedback")}
      }
    ]
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(/*options*/): void {

  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow(): void {

  },

  copyQQGroupId(): void {
    wx.setClipboardData({
      data: '1150057272',
      success: () => wx.showToast({ title: "已复制到剪贴板" })
    })
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {
    return {
      title: '发现',
      path: 'pages/explore/explore'
      + `?page=explore`,
      image: "images/logo.png"
    }
  }
})