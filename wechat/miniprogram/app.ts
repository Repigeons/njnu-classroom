// app.ts
App<IAppOption>({
  globalData: {
    server: 'https://classroom.njnu.xyz'
  },
  onLaunch() {
    this.clearStorage()
    this.preload()
  },

  clearStorage(): void {
    const keys = [
      'notice',
      'position.json',
      'classroom.json',
      'zylxdm.json',
      'last_overview',
      'explore/shuttle.json',
      'explore/grids.json',
    ]
    const storageInfo = wx.getStorageInfoSync().keys
    const storage: Record<string, any> = {}
    for (let key_index in keys) {
      const key = keys[key_index]
      if (storageInfo.indexOf(key) != -1) {
        storage[key] = wx.getStorageSync(key)
      }
    }
    wx.clearStorageSync()
    for (let key in storage) {
      wx.setStorage({ key, data: storage[key] })
    }
  },

  preload(): void {
    this.getPosition(true)
    this.getClassrooms(true)
    this.getZylxdm(true)
    this.getShuttle(true)
    this.getExploreGrids(true)
  },

  getNotice(): Promise<INotice> {
    return new Promise((resolve, reject) => {
      wx.request({
        url: `${this.globalData.server}/notice.json`,
        success: res => resolve(res.data as INotice),
        fail: reject
      })
    })
  },
  getPosition(request: boolean): Promise<IJxlPosition> {
    if (request) {
      wx.request({
        url: `${this.globalData.server}/position.json`,
        success: res => wx.setStorage({
          key: 'position.json',
          data: res.data
        }),
        fail: console.error
      })
    }
    return new Promise((resolve, reject) => {
      wx.getStorage({
        key: 'position.json',
        success: res => resolve(res.data),
        fail: () => wx.request({
          url: `${this.globalData.server}/position.json`,
          success: res => resolve(res.data as IJxlPosition),
          fail: reject
        })
      })
    })
  },
  getClassrooms(request: boolean): Promise<Record<string, Array<IJasInfo>>> {
    if (request) {
      wx.request({
        url: `${this.globalData.server}/classrooms.json`,
        success: res => wx.setStorage({
          key: 'classrooms.json',
          data: res.data
        }),
        fail: console.error
      })
    }
    return new Promise((resolve, reject) => {
      wx.getStorage({
        key: 'classrooms.json',
        success: res => resolve(res.data),
        fail: () => wx.request({
          url: `${this.globalData.server}/classrooms.json`,
          success: res => resolve(res.data as Record<string, Array<IJasInfo>>),
          fail: reject
        })
      })
    })
  },
  getZylxdm(request: boolean): Promise<Record<string, string>> {
    if (request) {
      wx.request({
        url: `${this.globalData.server}/zylxdm.json`,
        success: res => wx.setStorage({
          key: 'zylxdm.json',
          data: res.data
        }),
        fail: console.error
      })
    }
    return new Promise((resolve, reject) => {
      wx.getStorage({
        key: 'zylxdm.json',
        success: res => resolve(res.data),
        fail: () => wx.request({
          url: `${this.globalData.server}/zylxdm.json`,
          success: res => resolve(res.data as Record<string, string>),
          fail: reject
        })
      })
    })
  },
  getShuttle(request: boolean): Promise<IShuttle> {
    if (request) {
      wx.request({
        url: `${this.globalData.server}/explore/shuttle.json`,
        success: res => wx.setStorage({
          key: 'explore/shuttle.json',
          data: res.data
        }),
        fail: console.error
      })
    }
    return new Promise((resolve, reject) => {
      wx.getStorage({
        key: 'explore/shuttle.json',
        success: res => resolve(res.data),
        fail: () => wx.request({
          url: `${this.globalData.server}/explore/shuttle.json`,
          success: res => resolve(res.data as IShuttle),
          fail: reject
        })
      })
    })
  },
  getExploreGrids(request?: boolean): Promise<Array<IGrid>> {
    if (request) {
      wx.request({
        url: `${this.globalData.server}/explore-grids.json`,
        success: res => wx.setStorage({
          key: 'explore/grids.json',
          data: res.data
        }),
        fail: console.error
      })
    }
    return new Promise((resolve, reject) => {
      wx.getStorage({
        key: 'explore/grids.json',
        success: res => resolve(res.data),
        fail: () => wx.request({
          url: `${this.globalData.server}/explore-grids.json`,
          success: res => resolve(res.data as Array<IGrid>),
          fail: reject
        })
      })
    })
  }
})
