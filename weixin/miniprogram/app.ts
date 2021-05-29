// app.ts
import encrypt from "./utils/encrypt"

App<IAppOption>({
  globalData: {
    server: 'https://classroom.njnu.xyz'
  },
  
  onLaunch() {
    this.flushStorage()
    this.preload()
  },

  flushStorage(): void {
    const userData = [
      "last_overview",
      "notice",
    ],
    cache = [
      `${this.globalData.server}/static/classroom/position.json`,
      `${this.globalData.server}/static/classroom/list.json`,
      `${this.globalData.server}/static/classroom/zylxdm.json`,
      `${this.globalData.server}/static/explore/grids.json`,
      `${this.globalData.server}/explore/shuttle.json`,
    ]
    const storageInfo = wx.getStorageInfoSync().keys
    const storage: Record<string, any> = {}
    userData.forEach(key => {
      if (storageInfo.indexOf(key) != -1)
        storage[key] = wx.getStorageSync(key)
    })
    cache.forEach(url => {
      let key = encrypt(url)
      if (storageInfo.indexOf(key) != -1)
        storage[key] = wx.getStorageSync(key)
    })
    wx.clearStorageSync()
    for (let key in storage)
      wx.setStorage({ key, data: storage[key] })
  },

  preload(): void {
    this.getJxlPosition(true)
    this.getClassrooms(true)
    this.getZylxdm(true)
    this.getShuttle(true)
    this.getExploreGrids(true)
  },

  _getCache(args: {url: string, request: boolean}): Promise<string|Record<string,any>|ArrayBuffer> {
    let key = encrypt(args.url)
    if (args.request) {
      wx.request({
        url: args.url,
        success: res => wx.setStorage({
          key: key,
          data: res.data
        }),
        fail: console.error
      })
    }
    return new Promise((resolve, reject) => wx.getStorage({
      key: key,
      success: res => resolve(res.data),
      fail: () => wx.request({
        url: args.url,
        success: res => resolve(res.data),
        fail: reject
      })
    }))
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

  getJxlPosition(request: boolean): Promise<Array<IPosition>> {
    return new Promise((resolve, reject) => {
      this._getCache({
        url: `${this.globalData.server}/static/classroom/position.json`,
        request
      })
      .then (data => resolve(data as Array<IPosition>))
      .catch(reject)
    })
  },
  
  getClassrooms(request: boolean): Promise<Record<string, Array<IJasInfo>>> {
    return new Promise((resolve, reject) => {
      this._getCache({
        url: `${this.globalData.server}/static/classroom/list.json`,
        request
      })
      .then (data => resolve(data as Record<string, Array<IJasInfo>>))
      .catch(reject)
    })
  },
  
  getZylxdm(request: boolean): Promise<Array<KeyValue>> {
    return new Promise((resolve, reject) => {
      this._getCache({
        url: `${this.globalData.server}/static/classroom/zylxdm.json`,
        request
      })
      .then (data => resolve(data as Array<KeyValue>))
      .catch(reject)
    })
  },

  getExploreGrids(request: boolean): Promise<Array<IGrid>> {
    return new Promise((resolve, reject) => {
      this._getCache({
        url: `${this.globalData.server}/static/explore/grids.json`,
        request
      })
      .then (data => resolve(data as Array<IGrid>))
      .catch(reject)
    })
  },

  getShuttle(request: boolean): Promise<IShuttle> {
    return new Promise((resolve, reject) => {
      this._getCache({
        url: `${this.globalData.server}/explore/shuttle.json`,
        request
      })
      .then (data => resolve(data as IShuttle))
      .catch(reject)
    })
  },
})
