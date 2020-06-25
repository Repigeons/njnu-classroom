// index.js
// 获取应用实例
const app = getApp<IAppOption>()
import { distance, jc } from '../../utils/util.js'

// constant
const jxl = app.globalData.jxl

Page({
  data: {
    jxl_array: [undefined],
    jxl_selected: 0,

    rq_array: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
    rq_selected: 0,

    jc_array: ['第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节', '第11节', '第12节'],
    jc_selected: 0,
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名（仅用于列表显示）
   */
  onLoad() {
    let jxl_array = []
    for (let i = 0; i < jxl.length; i++)
      jxl_array.push(jxl[i].name)
    this.setData({jxl_array})
  },

  /**
   * 生命周期函数--监听页面显示
   * 每次显示时重置状态
   */
  onShow() {
    this.dangqianriqi()
    this.dangqianjieci()
    this.dingwei()
  },

  /**
   * 获取当前定位并选择最近的教学楼
   */
  dingwei() {
    wx.getLocation({
      type: 'gcj02',
      success: res => {
        let minId = 0
        let minDis = distance({
          longitude1: jxl[0].pos[1],
          latitude1: jxl[0].pos[0],
          longitude2: res.longitude,
          latitude2: res.latitude,
        })
        for (let i = 1; i < jxl.length; i++) {
          let dis = distance({
            longitude1: jxl[i].pos[1],
            latitude1: jxl[i].pos[0],
            longitude2: res.longitude,
            latitude2: res.latitude,
          })
          if (minDis > dis) {
            minDis = dis
            minId = i
          }
        }
        this.setData({ jxl_selected: minId })
        this.submit()
      },
      fail: err => console.error(err)
    })
  },

  /**
   * 将选择的日期设为当天
   */
  dangqianriqi() {
    this.setData({ rq_selected: new Date().getDay() })
    this.submit()
  },

  /**
   * 将选择的课程节次设为当前节次
   */
  dangqianjieci: function () {
    this.setData({ jc_selected: jc(new Date()) })
    this.submit()
  },

  /**
   * 选择教学楼
   */
  bindJxlChange: function (e: AnyObject) {
    this.setData({ jxl_selected: e.detail.value })
    this.submit()
  },

  /**
   * 选择日期
   */
  bindRqChange(e: AnyObject) {
    this.setData({ rq_selected: e.detail.value })
    this.submit()
  },

  /**
   * 选择节次
   */
  bindJcChange(e: AnyObject) {
    this.setData({ jc_selected: e.detail.value })
    this.submit()
  },

  /**
   * 提交请求至服务器，更新显示的数据
   */
  submit() {
    wx.request({
      url: app.globalData.server + '/index.json',
      dataType: 'json',
      data: {
        day: this.data.rq_selected,
        jxl: jxl[this.data.jxl_selected].name,
        dqjc: +this.data.jc_selected + 1
      },
      success: res => this.setData({ classroomList: res.data }),
      fail: err => {
        console.error(err)
        this.setData({ classroomList: [] })
      }
    })
  },
})
