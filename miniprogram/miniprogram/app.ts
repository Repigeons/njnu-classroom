// app.ts
import {
  getZylxdm,
  getJxlPosition,
  getClassrooms,
  getExploreGrids,
  getShuttle
} from "./utils/getCache"

App<IAppOption>({
  globalData: {
  },

  onLaunch() {
    const storageKeys = [
      "last_overview",
      "notice",
      "/api/zylxdm.json",
      "/api/position.json",
      "/api/classrooms.json",
      "/explore/grids.json",
      "/explore/shuttle.json?day=",
    ]
    wx.getStorageInfo({
      success(res) {
        res.keys.forEach(key => {
          const del = !storageKeys.includes(key)
          console.info("delete storage", key, del)
          if (del) wx.removeStorage({ key })
        })
      }
    })
    getZylxdm(true)
    getJxlPosition(true)
    getClassrooms(true)
    getExploreGrids(true);
    ["Sun.", "Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", ""].forEach(day => getShuttle(day, true))
  }
})