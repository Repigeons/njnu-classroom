// overview.ts
// 获取应用实例
const app = getApp<IAppOption>()
import { parseKcm, item2dialog } from '../../utils/parser'
import { getJc } from '../../utils/util'

Page({
  data: {
    // 选择教室
    classrooms: Object() as Record<string, Array<IJasInfo>>,
    jxl_array: Array<string>(),
    jxl_selected: 0,
    jsmph_selected: 0,
    // 布局
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
    // 结果集
    bar_list: Array<IClassroomRow>(),
    empty: true,
    dialog: {},
    closeDialog: [{text:"关闭"}],
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名（仅用于列表显示）
   */
  onLoad(options: Record<string, string>): void {
    const { windowHeight, windowWidth } = wx.getSystemInfoSync()
    const cellHeight = (windowHeight - (this.data.topBorder + 20)) / 13
    const cellWidth = (windowWidth - this.data.leftBorder * 2) / 8 - 1
    this.setData({ cellHeight, cellWidth })
    app.getClassrooms().then(data => this.setData({
      classrooms: data,
      jxl_array: Object.keys(data)
    }))

    if (options.page == 'overview') {
      let {jxlmc, jsmph} = options
      this.switchClassroom(jxlmc, jsmph)
    }
  },

  onShow(): void {
    this.setData({ dqjc: getJc(new Date()) })
    wx.getStorage({
      key: 'last_overview',
      success: res => {
        let {jxlmc, jsmph} = res.data
        this.switchClassroom(jxlmc, jsmph)
      },
      fail: () => this.bindJxlChange({detail:{value:0}})
    })
  },

  /**
   * 选择教学楼
   */
  bindJxlChange(e: any): void {
    this.setData({ jxl_selected: +e.detail.value })
    this.bindJsChange({detail:{value:0}})
  },

  /**
   * 选择教室
   */
  bindJsChange(e: any): void {
    let jsmph_selected = +e.detail.value,
        jxlmc = this.data.jxl_array[this.data.jxl_selected],
        jsmph = this.data.classrooms[jxlmc][jsmph_selected].JSMPH
    this.setData({ jsmph_selected })
    wx.setStorage({
      key: 'last_overview',
      data: { jxlmc, jsmph }
    })
    this.submit()
  },
  
  /**
   * 前一个教室
   */
  bindFormer(): void {
    let jasList = this.data.classrooms[this.data.jxl_array[this.data.jxl_selected]],
        value = (this.data.jsmph_selected - 1 + jasList.length) % jasList.length
    this.bindJsChange({detail:{value}})
  },
  /**
   * 后一个教室
   */
  bindLatter(): void {
    let jasList = this.data.classrooms[this.data.jxl_array[this.data.jxl_selected]],
        value = (this.data.jsmph_selected + 1) % jasList.length
    this.bindJsChange({detail:{value}})
  },

  submit() {
    let jxlmc = this.data.jxl_array[this.data.jxl_selected],
        jasdm = this.data.classrooms[jxlmc][this.data.jsmph_selected].JASDM
    wx.request({
      url: `${app.globalData.server}/api/overview.json`,
      data: { jasdm },
      success: res => {
        let resData = res.data as Record<string, any>
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

  /**
   * 显示详细信息
   */
  showDialog(e: any): void {
    const rq_array = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
    const index: number = e.currentTarget.dataset.index
    const item = this.data.bar_list[index]
    const rq: string = rq_array[item.day]
    this.setData({dialog: item2dialog(item, rq)})
  },
  closeDialog(): void {
    this.setData({dialog: {}})
  },

  switchClassroom(jxl: string, jsmph: string): void {
    let jxl_selected = 0, jsmph_selected = 0
    this.data.jxl_array.forEach((jxlmc, jxlIndex) => {
      if (jxlmc == jxl) jxl_selected = jxlIndex
    })
    this.data.classrooms[jxl].forEach((jas, jsmphIndex) => {
      if (jas.JSMPH == jsmph) jsmph_selected = jsmphIndex
    })
    this.setData({ jxl_selected, jsmph_selected })
    this.submit()
  },

  onShareAppMessage() {
    let jxlmc = this.data.jxl_array[this.data.jxl_selected],
        jsmph = this.data.classrooms[jxlmc][this.data.jsmph_selected].JSMPH
    return {
      title: '教室概览',
      path: 'pages/overview/overview'
      + `?page=overview`
      + `&jxlmc=${jxlmc}`
      + `&jsmph=${jsmph}`,
      image: 'images/logo.png'
    }
  }
})
export {}
