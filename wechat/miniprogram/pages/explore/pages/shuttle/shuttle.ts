// explore/pages/shuttlebus/shuttlebus.js
// 获取应用实例
const app = getApp<IAppOption>()
import {getDistance} from '../../../../utils/util'

Page({
  data: {
    selectedStation: 0,
    stations_display: Array<string>(),
    stations: Array<IShuttleStation>(),
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
    app.getShuttle().then((data: IShuttle) => {
      this.setData(data)
      let name2index: Record<string, number> = {}
      for (let stationIndex = 0; stationIndex < data.stations.length; stationIndex++) {
        name2index[data.stations[stationIndex][0]] = stationIndex
      }
      this.setData({ name2index })

      wx.getLocation({
        type: 'gcj02',
        success: res => {
          let stations_display: Array<string> = [],
              stationDistance: Array<number> = [],
              nearestStation: Array<{name:string, distance:number}> = []
          for (let stationIndex = 0; stationIndex < this.data.stations.length; stationIndex++) {
            let element = this.data.stations[stationIndex]
            let distance = Math.floor(getDistance({
              latitude1: element[1],
              longitude1: element[2],
              longitude2: res.longitude,
              latitude2: res.latitude,
            }))
            nearestStation.push({ name: element[0], distance })
            stationDistance.push(distance)
            stations_display.push(element[0])
          }
          nearestStation.sort((a,b)=>a.distance-b.distance)
          for (let index = 0; index < stations_display.length; index++) {
            if (stations_display[index] == nearestStation[0].name) {
              stations_display[index] += this.data.nearestHint
              this.setData({ selectedStation: index })
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
      this.setData({ direction: !this.data.direction})
    }
    if (!this.data.direction) {
      this.setData({
        terminus: this.data.stations[this.data.stations.length-1][0],
        routes: this.data.direction1
      })
    } else {
      this.setData({
        terminus: this.data.stations[0][0],
        routes: this.data.direction2
      })
    }
    // 滚动到最近位置
    let now = new Date()
    for (let scrollIndex = 0; scrollIndex < this.data.routes.length; scrollIndex++) {
      if (Date.parse(`0 ${this.data.routes[scrollIndex][0]}`) - Date.parse(`0 ${now.getHours()}:${now.getMinutes()}`) >= -15) {
        this.setData({ scrollId: `row${scrollIndex ? scrollIndex-1 : scrollIndex}` })
        break
      }
    }
  },

  bindStationChange(e: AnyObject): void {
    this.setData({ selectedStation: +e.detail.value })
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
