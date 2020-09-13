// app.ts
App<IAppOption>({
  globalData: {
    server: 'https://classroom.njnu.xyz',
    jxl: [
      { name: '学明楼', pos: [32.10202, 118.91082] },
      { name: '学正楼', pos: [32.10259, 118.91246] },
      { name: '学海楼', pos: [32.10201, 118.91417] },
      { name: '广乐楼', pos: [32.10465, 118.91303] },
      { name: '学行楼', pos: [32.11415, 118.91483] },
      { name: '学思楼', pos: [32.11552, 118.90870] },
      { name: '信息楼', pos: [32.05445, 118.77064] },
      { name: '电教楼', pos: [32.05454, 118.76777] },
    ],
    lx: [
      { dm: '#', name: '所有' },
      { dm: '01', name: '本科生课程' },
      { dm: '02', name: '本科生考试' },
      { dm: '04', name: '活动/借用' },
      { dm: '05', name: '其他' },
      { dm: '10', name: '研究生课程' },
    ],
    classrooms: {}
  },
  onLaunch() {
    this.globalData.classrooms = wx.getStorageSync('classrooms')
    wx.request({
      url: `${this.globalData.server}/classrooms.json`,
      success: res =>  {
        this.globalData.classrooms = res.data as Record<string, Array<AnyObject>>
        wx.setStorageSync('classrooms', res.data)
      }
    })
  }
})