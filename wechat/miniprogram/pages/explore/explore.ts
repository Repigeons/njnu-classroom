// explore.ts
// 获取应用实例
const app = getApp<IAppOption>()

Page({
  /**
   * 页面的初始数据
   */
  data: {
    fullYear: new Date().getFullYear(),
    grids: Array<Record<string,string>>()
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad(/*options*/): void {
    wx.request({
      url: `${app.globalData.server}/explore-grids.json`,
      success: res => {
        this.setData({ grids: res.data as Array<Record<string,string>>})
      }
    })
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
export {}
