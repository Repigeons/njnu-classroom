export { }
// explore/shuttlebus
import { getDistance } from '../../../../utils/util'
import { parseTime } from "../../../../utils/parser"
import { getShuttle } from '../../../../utils/getCache'
import { uploadFile } from '../../../../utils/http'

Page({
  data: {
    /**显示周几*/
    rq_array: [
      { key: 'Mon.', value: "周一" },
      { key: 'Tue.', value: "周二" },
      { key: 'Wed.', value: "周三" },
      { key: 'Thu.', value: "周四" },
      { key: 'Fri.', value: "周五" },
      { key: 'Sat.', value: "周六" },
      { key: 'Sun.', value: "周日" },
    ] as Array<KeyValue>,
    day_selected: 0,
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

    name2Number: Object() as Record<string, number>,

    nearestHint: "(最近)",
  },

  onShow() {
    wx.getLocation({
      type: 'gcj02',
      success: async (res) => {
        const iShuttle = await getShuttle(this.data.rq_array[0].key)
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
        const name2Number: Record<string, number> = Object()
        stations.forEach(v => name2Number[v.name] = v.number)
        this.setData({ stations, name2Number, station_selected: stations.findIndex(v => v.name != v.rangeKey) })
        this.bindWeekChange({ detail: { value: (new Date().getDay() + 6) % 7 } })
      },
      fail: console.error
    })
  },

  redirect(e?: boolean) {
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
      if (parseTime(this.data.routes[scrollIndex].startTime) - parseTime(`${now.getHours()}:${now.getMinutes()}`) < -15) {
        break
      }
      scrollIndex--
    }
    this.setData({ scrollId: `row${scrollIndex}` })
  },

  bindStationChange(e: { detail: { value: number } }) {
    this.setData({ station_selected: +e.detail.value })
  },

  async bindWeekChange(e: { detail: { value: number } }) {
    const day_selected = +e.detail.value
    this.setData({ day_selected: day_selected })
    const shuttle = await getShuttle(this.data.rq_array[day_selected].key)
    this.setData({
      direction1: shuttle.direction1,
      direction2: shuttle.direction2,
    })
    this.redirect()
  },

  async uploadFile() {
    const res = await wx.chooseImage({ count: 1 }) as any
    await uploadFile({
      path: "/explore/shuttle/upload",
      filePath: res.tempFiles[0].path,
    })
    wx.showToast({ title: '上传成功！' })
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
