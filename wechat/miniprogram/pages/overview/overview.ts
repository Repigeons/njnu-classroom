// index.ts
// 获取应用实例
const app = getApp<IAppOption>()

Page({
  data: {
    cellHeight: 0,
    cellWidth: 0,
    leftBorder: 8,
    topBorder: 56,
    jc_array: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名（仅用于列表显示）
   */
  onLoad(): void {
    const { windowHeight, windowWidth } = wx.getSystemInfoSync()
    let cellHeight = (windowHeight - (this.data.topBorder + 20)) / 13
    let cellWidth = (windowWidth - this.data.leftBorder * 2) / 8 - 1

    this.setData({ cellHeight, cellWidth })
  },
})
