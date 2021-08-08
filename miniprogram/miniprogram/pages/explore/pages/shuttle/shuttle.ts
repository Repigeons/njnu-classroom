export { }
// explore/shuttlebus
import { getDistance } from '../../../../utils/util'
import parseTime from "../../../../utils/timeParser"
import { getShuttle } from '../../../../utils/getCache'
// 获取应用实例
const app = getApp<IAppOption>()

Page({
  data: {
    station_selected: 0,
    stations_display: Array<string>(),
    week_selected: 0,
    week_display: ['周一','周二','周三','周四','周五','周六','周日'],
    stations: Array<IPosition>(),
    routes: Array<IShuttleRoute>(),
    direction1: Array<IShuttleRoute>(),
    direction2: Array<IShuttleRoute>(),
    direction: Boolean(),
    terminus: String(),
    scrollId: String(),
    name2index: Object() as Record<string, number>,
    stationDistance: Array<number>(),

    nearestHint: "（离我最近）",
  },

  onShow() {
    getShuttle().then((data: IShuttle) => {
      let name2index: Record<string, number> = {}
      data.stations.forEach((station, index) => name2index[station.name] = index)
      this.setData(data)
      this.setData({ name2index })

      wx.getLocation({
        type: 'gcj02',
        success: res => {
          let stations_display: Array<string> = [],
            stationDistance: Array<number> = [],
            nearestStation: Array<{ name: string, distance: number }> = []
          this.data.stations.forEach(station => {
            let distance = Math.floor(getDistance({
              latitude1: station.position[0],
              longitude1: station.position[1],
              longitude2: res.longitude,
              latitude2: res.latitude,
            }))
            nearestStation.push({ name: station.name, distance })
            stationDistance.push(distance)
            stations_display.push(station.name)
          })
          nearestStation.sort((a, b) => a.distance - b.distance)
          for (let index = 0; index < stations_display.length; index++) {
            if (stations_display[index] == nearestStation[0].name) {
              stations_display[index] += this.data.nearestHint
              this.setData({ station_selected: index })
              break
            }
          }
          this.setData({ stations_display, stationDistance })
          this.redirect()
        },
        fail: console.error
      })
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
    let now = new Date(), scrollIndex = this.data.routes.length - 1
    while (scrollIndex > 0) {
      if (parseTime(this.data.routes[scrollIndex][0]) - parseTime(`${now.getHours()}:${now.getMinutes()}`) < -15) {
        break
      }
      scrollIndex--
    }
    this.setData({ scrollId: `row${scrollIndex}` })
  },

  bindStationChange(e: AnyObject): void {
    this.setData({ station_selected: +e.detail.value })
  },

  bindWeekChange(e: AnyObject): void {
    this.setData({ week_selected: +e.detail.value })
    //TODO:需要实现选择特定星期后，服务端返回选择星期对应的校车时刻表
    //下面交给下一任开发者继续完成
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
    // 发送文件到服务器
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
