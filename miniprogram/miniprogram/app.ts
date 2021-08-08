// app.ts
import encrypt from "./utils/encrypt"
import {
  initialize,
  getJxlPosition,
  getClassrooms,
  getZylxdm,
  getExploreGrids
} from "./utils/getCache"

const useDevelopServer: boolean = false

App<IAppOption>({
  globalData: {
    server: useDevelopServer ? 'https://t-classroom.njnu.xyz' : 'https://classroom.njnu.xyz'
  },

  onLaunch() {
    initialize(this)
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
      const key = encrypt(url)
      if (storageInfo.indexOf(key) != -1)
        storage[key] = wx.getStorageSync(key)
    })
    wx.clearStorageSync()
    for (const key in storage)
      wx.setStorage({ key, data: storage[key] })
  },

  preload(): void {
    getJxlPosition(true)
    getClassrooms(true)
    getZylxdm(true)
    getExploreGrids(true)
  }
})
