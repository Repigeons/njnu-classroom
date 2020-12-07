// app.ts
App<IAppOption>({
  globalData: {
    server: 'https://classroom.njnu.xyz',
    zylxdm: Object(),
    classrooms: Object(),
  },
  onLaunch() {
    this.getClassrooms().then(data => this.globalData.classrooms = data)
    this.getZylxdm().then(data => this.globalData.zylxdm = data)
  },
  getNotice() {
    return new Promise((resolve) => {
      wx.request({
        url: `${this.globalData.server}/notice.json`,
        success: res => resolve(res.data as INotice)
      })
    })
  },
  getPositionJson() {
    wx.request({
      url: `${this.globalData.server}/position.json`,
      success: res => wx.setStorage({
        key: 'position.json',
        data: res.data
      }),
      fail: console.error
    })
    return new Promise((resolve) => {
      wx.getStorage({
        key: 'position.json',
        success: res => resolve(res.data),
        fail: () => wx.request({
          url: `${this.globalData.server}/position.json`,
          success: res => resolve(res.data as IJxlPosition)
        })
      })
    })
  },
  getClassrooms() {
    wx.request({
      url: `${this.globalData.server}/classrooms.json`,
      success: res => wx.setStorage({
        key: 'classrooms.json',
        data: res.data
      }),
      fail: console.error
    })
    return new Promise((resolve) => {
      wx.getStorage({
        key: 'classrooms.json',
        success: res => resolve(res.data),
        fail: () => wx.request({
          url: `${this.globalData.server}/classrooms.json`,
          success: res => resolve(res.data as Record<string, Array<IJasInfo>>)
        })
      })
    })
  },
  getZylxdm() {
    wx.request({
      url: `${this.globalData.server}/zylxdm.json`,
      success: res => wx.setStorage({
        key: 'zylxdm.json',
        data: res.data
      }),
      fail: console.error
    })
    return new Promise((resolve) => {
      wx.getStorage({
        key: 'zylxdm.json',
        success: res => resolve(res.data),
        fail: () => wx.request({
          url: `${this.globalData.server}/zylxdm.json`,
          success: res => resolve(res.data as Record<string, string>)
        })
      })
    })
  } 
})
