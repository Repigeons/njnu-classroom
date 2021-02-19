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
        url: "pages/searchmore/searchmore",
        text: "更多搜索",
        imgUrl: "/images/gdss.png",
      },
      {
        url: "pages/shuttle/shuttle",
        text: "校内班车时刻表",
        imgUrl: "/images/gdss.png",
      },
      {
        url: "pages/calendar/calendar",
        text: "校历",
        imgUrl: "/images/gdss.png",
      },
      {
        url: ".",
        text: "定制时间表",
        imgUrl: "/images/gdss.png",
      },
      {
        url: ".",
        text: "一键支持",
        imgUrl: "/images/gdss.png",
      },
      {
        url: ".",
        text: "反馈",
        imgUrl: "/images/gdss.png",
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