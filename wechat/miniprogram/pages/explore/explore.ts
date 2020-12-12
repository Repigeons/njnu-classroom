// explore.ts
// 获取应用实例
// const app = getApp<IAppOption>()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    grids: [
      {
        "pagePath": "pages/searchmore/searchmore",
        "iconPath": "/images/gdss.png",
        "text": "更多搜索"
      },
      {
        "pagePath": "pages/shuttle/shuttle",
        "iconPath": "/images/gdss.png",
        "text": "校内班车时刻表"
      },
      {
        "pagePath": "pages/calendar/calendar",
        "iconPath": "/images/gdss.png",
        "text": "校历"
      },
      {
        "pagePath": ".",
        "iconPath": "/images/gdss.png",
        "text": "定制时间表"
      },
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

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {
    return {
      title: '发现',
      path: 'pages/explore/explore'
      + `?page=explore`,
      image: 'images/logo.png'
    }
  }
})