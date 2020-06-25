// pages/searchmore/searchmore.js
// 获取应用实例
const app = getApp<IAppOption>()
import { parseKCM, item2dialog } from '../../utils/parser'

// constant
const jxl = app.globalData.jxl
const lx = app.globalData.lx
const perPage = 50

Page({
  data: {
    jxl_array: [''],
    jxl_selected: 0,

    rq_array: ['所有', '周日', '周一', '周二', '周三', '周四', '周五', '周六'],
    rq_selected: 0,

    jc_array: ['第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节', '第11节', '第12节'],
    jc_ks_selected: 0, jc_js_selected: 11,
    jc_js_array: [''],
    jc_ks_array: [''],

    lx_array: [undefined],
    lx_selected: 0,

    keyword: '',

    inputShowed: false,
    buttonShowed: false,
    resultsShowed: false,

    iconPath: {
      '01': '/images/benke.png',
      '03': '/images/benke.png',
      '02': '/images/jieyong.png',
      '04': '/images/jieyong.png',
      '05': '/images/qita.png',
      '10': '/images/yanjiusheng.png',
      '11': '/images/yanjiusheng.png',
    },
    showDialog: false,
    dialog: {},
    list: []
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名、类型吗（仅用于列表显示）
   * 初始化可选节次数组
   */
  onLoad: function () {
    let jxl_array = ['所有'], lx_array = []
    for (let i = 0; i < jxl.length; i++)
      jxl_array.push(jxl[i].name)
    for (let i = 0; i < lx.length; i++)
      lx_array.push(lx[i].name)
    this.setData({jxl_array, lx_array})

    this.updateJcArray()
  },

  /**
   * 更新节次列表
   */
  updateJcArray: function () {
    let jc_ks_array = [], jc_js_array = []
    for (let i = 0; i <= this.data.jc_js_selected; i++)
      jc_ks_array.push(this.data.jc_array[i])
    for (let i = this.data.jc_ks_selected; i < 12; i++)
      jc_js_array.push(this.data.jc_array[i])
    this.setData({
      jc_ks_array: jc_ks_array,
      jc_js_array: jc_js_array
    })
  },

  /**
   * 显示输入框
   */
  showInput: function () {
    this.setData({
      inputShowed: true,
      buttonShowed: true,
      resultsShowed: false
    })
  },

  /**
   * 显示按钮
   */
  showButton: function () {
    this.setData({
      buttonShowed: true,
      resultsShowed: false
    })
  },

  /**
   * 搜索
   */
  onSearch: function () {
    this.setData({ buttonShowed: false })
    if (this.data.keyword) {
      wx.request({
        url: app.globalData.server + '/searchmore.json',
        dataType: 'json',
        data:{
          day: (this.data.rq_selected == 0) ? '#' : this.data.rq_selected - 1,
          jc_ks: this.data.jc_ks_selected + 1,
          jc_js: this.data.jc_js_selected + 1,
          jxl: (this.data.jxl_selected == 0) ? '#' : jxl[this.data.jxl_selected].name,
          zylxdm: lx[this.data.lx_selected].dm,
          kcm: this.data.keyword
        },
        success: (res: AnyObject) => {
          for (let i = 0; i < res.data.length; i++) {
            let param: AnyObject = parseKCM(res.data[i].zylxdm, res.data[i].kcm)
            for (let k in param)
              res.data[i][k] = param[k]
            res.data[i].day = +res.data[i].day + 1
          }
          this.setData({
            list: res.data.slice(0, perPage),
            list_length: res.data.length,
            resultsShowed: true
          })
          wx.setStorage({
            key: 'list',
            data: res.data
          })
        },
        fail: res => {
          console.error(res)
          this.setData({ list: [] })
        }
      })
    }
  },

  /**
   * 清空输入框
   */
  clearInput: function () {
    this.setData({ keyword: '' })
  },

  /**
   * 输入搜索关键词
   */
  onInput: function (e: AnyObject) {
    this.setData({ keyword: e.detail.value.trim() })
  },

  /**
   * 选择日期
   */
  bindRqChange: function (e: AnyObject) {
    this.setData({ rq_selected: e.detail.value })
  },

  /**
   * 选择开始节次
   */
  bindJcKsChange: function (e: AnyObject) {
    this.setData({ jc_ks_selected: +e.detail.value })
    this.updateJcArray()
  },

  /**
   * 选择结束节次
   */
  bindJcJsChange: function (e: AnyObject) {
    this.setData({ jc_js_selected: +e.detail.value + 12 - this.data.jc_js_array.length })
    this.updateJcArray()
  },

  /**
   * 选择教学楼
   */
  bindJxlChange: function (e: AnyObject) {
    this.setData({ jxl_selected: +e.detail.value })
  },

  /**
   * 选择类型
   */
  bindLxChange: function (e: AnyObject) {
    this.setData({ lx_selected: +e.detail.value })
  },

  onReachBottom: function () {
    wx.getStorage({
      key: 'list',
      success: res => {
        let list = this.data.list
        this.setData({
          list: list.concat(res.data.slice(list.length, list.length+perPage))
        })
      }
    })
  },

  /**
   * 显示详细信息
   */
  showDialog: function (e: AnyObject) {
    const index = +e.currentTarget.dataset.index
    const item: AnyObject = this.data.list[index]
    const rq = this.data.rq_array[item.day]
    this.setData({ dialog: item2dialog(item, rq) })
    // console.log(item)
  },

  closeDialog: function () {
    this.setData({ dialog: {} })
  }
})
