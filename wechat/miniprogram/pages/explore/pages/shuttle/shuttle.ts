// explore/pages/shuttlebus/shuttlebus.js
// 获取应用实例
const app = getApp<IAppOption>()
import {formatTime, getTimeSpan, getDistance} from '../../../../utils/util'

Page({
  data: {
    showMoreStation: false,
    stations_display: Array<string>(),
    routes: Object(),
    stations: Object(),
    routes1: Object(),
    routes2: Object(),
    direction: Boolean(),
    hasBus: Boolean(),
    start: String(),
    end: String(),
    nextShuttle: Number(),
    intervalUpdate: Array<number>(),
  },
  
  onLoad(/*options*/) {
  },
  
  onShow() {
    app.getShuttle().then(data => {
      this.setData(data)
      let stations_display: Array<string> = []
      wx.getLocation({
        type: 'gcj02',
        success: res => {
          let list = []
          for (let station in this.data.stations) {
            let distance: number = getDistance({
              latitude1: this.data.stations[station][0],
              longitude1: this.data.stations[station][1],
              longitude2: res.longitude,
              latitude2: res.latitude,
            })
            list.push({ station, distance })
          }
          list.sort((a,b)=>a.distance-b.distance)
          list.forEach(item => {
            stations_display.push(`${item.station}\t距离约${Math.floor(item.distance)}米`)
          })
          stations_display[0] += "（距离最近）"
          this.setData({ stations_display })
        },
        fail: console.error
      })

      this.direct()
    })
    setInterval(this.intervalUpdate, 1000 * 30)
  },

  direct(e?: any): void {
    if (e) {
      this.setData({ direction: !this.data.direction})
    }
    const now = new Date()
    const day = now.getDay()
    const time = formatTime(now)
    let stations = Object.keys(this.data.stations)
    this.setData({
      hasBus: day>0 && day<6,
      start: !this.data.direction ? stations[0] : stations[stations.length-1],
      end: !this.data.direction ? stations[stations.length-1] : stations[0],
    })
    let nextShuttle: number = -1,
        routes: Array<Array<string>> = !this.data.direction
        ? this.data.routes1
        : this.data.routes2
    if (time < routes[0][0]) {
      nextShuttle = 0
    } else if (time > routes[routes.length-1][0]) {
      nextShuttle = routes.length
    }
    for (let i=1; i<routes.length;i++) {
      if (routes[i-1][0]<=time && routes[i][0]>=time) {
        nextShuttle = i
      }
    }
    this.setData({ nextShuttle, routes })
    this.intervalUpdate()
  },

  showMoreStation() {
    this.setData({ showMoreStation: !this.data.showMoreStation })
  },

  intervalUpdate() {
    const nextShuttle = this.data.nextShuttle
    if (nextShuttle != -1) {
      const now = new Date()
      const timeSpan = getTimeSpan(now.getHours(), now.getMinutes())
      let lastShuttleTime = (nextShuttle>0) ? this.data.routes[nextShuttle-1][0].split(':') : ':',
          nextShuttleTime = (nextShuttle<this.data.routes.length) ? this.data.routes[nextShuttle][0].split(':') : ':'
      this.setData({ intervalUpdate: [
          timeSpan - getTimeSpan(+lastShuttleTime[0], +lastShuttleTime[1]),
          getTimeSpan(+nextShuttleTime[0], +nextShuttleTime[1]) - timeSpan
      ]})
    }
  },

  onShareAppMessage() {
    return {
      title: '校内班车',
      path: 'pages/explore/pages/shuttle/shuttle'
      + `?page=shuttle`,
      image: 'images/logo.png'
    }
  }
})
