export { }
// explore/shuttlebus
import { getDistance } from '../../../../utils/util'
import parseTime from "../../../../utils/timeParser"
import { getShuttle } from '../../../../utils/getCache'
// 获取应用实例
const app = getApp<IAppOption>()

Page({
  data: {
    /**显示周几*/
    day_selected: 0,
    day_display: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
    /**显示的车站*/
    station_selected: 0,
    /**车站列表*/
    stations: Array<IPosition>(),
    /**当前显示的校车时刻表*/
    routes: Array<IShuttleRoute>(),
    /**当日的车次1*/
    direction1: Array<IShuttleRoute>(),
    /**当日的车次2*/
    direction2: Array<IShuttleRoute>(),
    /**方向*/
    direction: Boolean(),
    /**终点站*/
    terminus: String(),
    /**滚动位置*/
    scrollId: String(),

    name2Number: {} as Record<string, number>,

    nearestHint: "(最近)",
  },

  onShow() {
    wx.getLocation({
      type: 'gcj02',
      success: async (res) => {
        const iShuttle = await getShuttle(0)
        const stations: Array<IPosition> = iShuttle.stations.map((station: IPosition, index: number) => {
          const distance = Math.floor(getDistance({
            latitude1: station.position[0],
            longitude1: station.position[1],
            longitude2: res.longitude,
            latitude2: res.latitude,
          }))
          return {
            name: station.name,
            rangeKey: station.name,
            position: station.position,
            distance: distance,
            number: index
          }
        })
        stations.sort((a, b) => a.distance - b.distance)
        stations[0].rangeKey += this.data.nearestHint
        stations.sort((a, b) => a.number - b.number)
        const name2Number: Record<string, number> = {}
        stations.forEach(v => name2Number[v.name] = v.number)
        this.setData({ stations, name2Number, station_selected: stations.findIndex(v => v.name != v.rangeKey) })
        this.bindWeekChange({ detail: { value: (new Date().getDay() + 6) % 7 } })
      },
      fail: console.error
    })
  },

  redirect(e?: boolean): void {
    if (e) {
      this.setData({ direction: !this.data.direction })
    }
    if (!this.data.direction) {
      this.setData({
        terminus: this.data.stations[this.data.stations.length - 1].name,
        routes: this.data.direction1
      })
    } else {
      this.setData({
        terminus: this.data.stations[0].name,
        routes: this.data.direction2
      })
    }
    // 滚动到最近位置
    const now = new Date()
    let scrollIndex = this.data.routes.length - 1
    while (scrollIndex > 0) {
      if (parseTime(this.data.routes[scrollIndex][0]) - parseTime(`${now.getHours()}:${now.getMinutes()}`) < -15) {
        break
      }
      scrollIndex--
    }
    this.setData({ scrollId: `row${scrollIndex}` })
  },

  bindStationChange(e: { detail: { value: number } }): void {
    this.setData({ station_selected: +e.detail.value })
  },

  bindWeekChange(e: { detail: { value: number } }): void {
    const week_selected = +e.detail.value
    this.setData({ day_selected: week_selected })
    getShuttle(week_selected).then(iShuttle => {
      this.setData({
        direction1: iShuttle.direction1,
        direction2: iShuttle.direction2,
      })
      this.redirect()
    })
    this.redirect()
  },

  uploadFile() {
    wx.chooseImage({
      count: 1,
      fail: console.error,
      success: (res) => {
        wx.uploadFile({
          url: `${app.globalData.server}/explore/shuttle/upload`,
          filePath: res.tempFiles[0].path,
          name: 'file',
          success: () => {
            wx.showToast({ title: '上传成功！' })
          },
          fail: console.error,
        })
      }
    })
  },

  onShareAppMessage() {
    return {
      title: '校内班车时刻表',
      path: 'pages/explore/pages/shuttle/shuttle'
        + `?page=shuttle`,
      image: 'images/logo.png'
    }
  }
})
