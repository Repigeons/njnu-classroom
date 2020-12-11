// overview.ts
// 获取应用实例
const app = getApp<IAppOption>()
import { parseKcm, item2dialog } from '../../utils/parser'
import { IClassroomRow } from '../../../typings/IClassroomInfo'
import { getJc } from '../../utils/util'

Page({
  data: {
    cellHeight: 0,
    cellWidth: 0,
    leftBorder: 8,
    topBorder: 56,
    barRatio: 0.8,
    dqjc: 1,
    // 周日->0
    day: new Date().getDay(),
    time_array: [
      ['08:00', '08:40'], ['08:45', '09:25'], ['09:40', '10:20'], ['10:35', '11:15'], ['11:20', '12:00'],
      ['13:30', '14:10'], ['14:15', '14:55'], ['15:10', '15:50'], ['15:55', '16:35'],
      ['18:30', '19:10'], ['19:20', '20:00'], ['20:10', '20:50'],
    ],

    classrooms: Object() as Record<string, Array<IJasInfo>>,
    jxl_name_array: Array<string>(),
    jxl_selected: 0,
    jsmph_array: Array<string>(),
    jsmph_selected: 0,
    dialog: {},
    bar_list: Array<IClassroomRow>(),
    empty: true,
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名（仅用于列表显示）
   */
  onLoad(options: Record<string, string>): void {
    const { windowHeight, windowWidth } = wx.getSystemInfoSync()
    let cellHeight = (windowHeight - (this.data.topBorder + 20)) / 13
    let cellWidth = (windowWidth - this.data.leftBorder * 2) / 8 - 1
    this.setData({ cellHeight, cellWidth })
    app.getClassrooms().then(data => this.setData({
      classrooms: data,
      jxl_name_array: Object.keys(data)
    }))

    if (options.page == 'overview') {
      const {JXLMC, JSMPH} = options
      this.switchClassroom(JXLMC, JSMPH)
    }
  },

  onShow(): void {
    this.setData({ dqjc: getJc(new Date()) })
    wx.getStorage({
      key: 'last_overview',
      success: res => {
        let {jxl, js} = res.data
        this.switchClassroom(jxl, js)
      },
      fail: () => this.bindJxlChange({detail:{value:0}})
    })
  },

  /**
   * 选择教学楼
   */
  bindJxlChange(e: AnyObject): void {
    const jxl_selected = +e.detail.value
    const jxl = this.data.jxl_name_array[jxl_selected]
    const list = this.data.classrooms[jxl]
    let jsmph_array = []
    for (let i=0; i< list.length; i++) {
      jsmph_array.push(list[i]['JSMPH'])
    }
    this.setData({ jxl_selected, jsmph_array })
    this.bindJsChange(0)
  },

  /**
   * 选择教室
   */
  bindJsChange(e: AnyObject): void {
    const jsmph_selected = (typeof e == 'number') ? e : +e.detail.value
    this.setData({ jsmph_selected })
    wx.setStorage({
      key: 'last_overview',
      data: {
        jxl: this.data.jxl_name_array[this.data.jxl_selected],
        js: this.data.jsmph_array[this.data.jsmph_selected],
      }
    })
    
    wx.request({
      url: `${app.globalData.server}/api/overview.json`,
      data: {
        jasdm: this.data.classrooms[this.data.jxl_name_array[this.data.jxl_selected]][jsmph_selected]['JASDM']
      },
      success: res => {
        let resData = res.data as Record<string, AnyObject>
        let bar_list = resData.data as Array<IClassroomRow>
        let kcmclimit = 0
        for (let i = 0; i < bar_list.length; i++) {
          switch (bar_list[i].zylxdm) {
            case '00':
              bar_list[i].usage = 'empty'
              break;
            case '01':
            case '03':
            case '10':
            case '11':
              bar_list[i].usage = 'class'
              break;
            default:
              bar_list[i].usage = 'others'
              break;
          }
          if (bar_list[i].day == this.data.day)
          if (bar_list[i].jc_ks <= this.data.dqjc + 1)
          if (bar_list[i].jc_js >= this.data.dqjc + 1) {
            this.setData({ empty: bar_list[i].zylxdm == '00' })
          }
          // day1: 周一~0
          bar_list[i].day1 = (bar_list[i].day + 6) % 7
          let info = parseKcm(bar_list[i].zylxdm, bar_list[i].kcm)
          if (info == null) continue
          for (let k in info) {
            bar_list[i][k] = info[k]
          }
          kcmclimit = (this.data.cellHeight * (bar_list[i].jc_js - bar_list[i].jc_ks + 1)) / (this.data.cellWidth * this.data.barRatio/3*1.3) * 3
          bar_list[i].shortkcmc = bar_list[i].title.length > kcmclimit ? bar_list[i].title.substring(0, kcmclimit - 3) + '...' : bar_list[i].title
        }
        this.setData({ bar_list })
      },
      fail: err => console.error(err)
    })
  },

  bindFormer(): void {
    let value = (this.data.jsmph_selected - 1 + this.data.jsmph_array.length) % this.data.jsmph_array.length
    this.bindJsChange(value)
  },

  bindLatter(): void {
    let value = (this.data.jsmph_selected + 1) % this.data.jsmph_array.length
    this.bindJsChange(value)
  },

  /**
   * 显示详细信息
   */
  showDialog(e: AnyObject): void {
    const rq_array = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    const index: number = e.currentTarget.dataset.index
    const item = this.data.bar_list[index]
    const rq: string = rq_array[item.day]
    this.setData({dialog: item2dialog(item, rq)})
  },

  closeDialog(): void {
    this.setData({dialog: {}})
  },

  switchClassroom(jxl: string, js: string): void {
    let jsmph_array = [], jxl_selected = 0, jsmph_selected = 0
    
    for (let i=0; i<this.data.jxl_name_array.length; i++) {
      if (this.data.jxl_name_array[i] == jxl) {
        jxl_selected = i
        break
      }
    }
    let list = this.data.classrooms[this.data.jxl_name_array[jxl_selected]]
    for (let i=0; i< list.length; i++) {
      jsmph_array.push(list[i]['JSMPH'])
      if (list[i]['JSMPH'] == js)
        jsmph_selected = i
    }
    this.setData({ jxl_selected, jsmph_array })
    this.bindJsChange(jsmph_selected)
  },

  onShareAppMessage() {
    return {
      title: '教室概览',
      path: 'pages/overview/overview'
      + `?page=overview`
      + `&JXLMC=${this.data.jxl_name_array[this.data.jxl_selected]}`
      + `&JSMPH=${this.data.jsmph_array[this.data.jsmph_selected]}`,
      image: 'images/logo.png'
    }
  }
})
