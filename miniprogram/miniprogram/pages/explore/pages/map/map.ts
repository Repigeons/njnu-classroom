import { getJxlPosition, getShuttle } from "../../../../utils/getCache"

// pages/explore/pages/map/map.ts
Page({

  /**
   * 页面的初始数据
   */
  data: {
    markers: Array(),
    campusPosition: [
      { latitude: 32.10800, longitude: 118.90880, },
      { latitude: 32.05294, longitude: 118.76763, }
    ],
    campusList: ["仙林校区", "随园校区"],
    campusSelected: 0,
    jxlPosition: Array<IPosition>(),
    entityList: ["教学楼", "校车站"],
    entitySelected: 0,
    shuttlePosition: Array<IPosition>(),
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad() {
    this.preloadInfo()
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  async preloadInfo() {
    const jxlPosition = await getJxlPosition()
    const shuttlePosition = (await getShuttle('')).stations
    this.setData({ jxlPosition, shuttlePosition })
    console.debug('jxlPosition', jxlPosition)
    console.debug('shuttlePosition', shuttlePosition)
    this.bindEntityChange({ detail: { value: this.data.entitySelected } })
  },

  bindCampusChange(e: any) {
    const value = +e.detail.value
    this.setData({
      campusSelected: value
    })
  },

  bindEntityChange(e: any) {
    const value = +e.detail.value
    if (value === 1)
      this.setData({ campusSelected: 0 })
    this.setData({
      entitySelected: value
    })
    switch (value) {
      case 0: {
        const markers = this.data.jxlPosition.map((item, index) => {
          return {
            id: index,
            latitude: item.position[0],
            longitude: item.position[1],
            title: item.name
          }
        })
        this.setData({ markers })
        break
      }
      case 1: {
        const markers = this.data.shuttlePosition.map((item, index) => {
          return {
            id: index,
            latitude: item.position[0],
            longitude: item.position[1],
            title: item.name
          }
        })
        this.setData({ markers })
        break
      }
    }
  },

  startNavigation(e: any) {
    const markerId = e.detail.markerId
    switch (this.data.entitySelected) {
      case 0: {
        const position = this.data.jxlPosition[markerId]
        wx.openLocation({
          latitude: position.position[0],
          longitude: position.position[1],
          name: position.name
        })
        break
      }
      case 1: {
        const position = this.data.shuttlePosition[markerId]
        wx.openLocation({
          latitude: position.position[0],
          longitude: position.position[1],
          name: position.name
        })
        break
      }
    }
  },

  onShareAppMessage() {
    return {
      title: '校园地图',
      path: 'pages/explore/pages/map/map'
        + `?page=map`,
      image: 'images/logo.png'
    }
  }
})