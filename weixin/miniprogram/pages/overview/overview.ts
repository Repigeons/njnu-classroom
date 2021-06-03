// overview
import { getClassrooms } from '../../utils/getCache'
import { parseKcm, item2dialog } from '../../utils/parser'
import { getJc } from '../../utils/util'
// 获取应用实例
const app = getApp<IAppOption>()

Page({
  data: {
    // 选择教室
    classrooms: Object() as Record<string, Array<IJasInfo>>,
    selecter: [Array(), Array()],
    selected: [0, 0],
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
    dialog_buttons: Array<IButton>(),
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

    getClassrooms().then(data => {
      const jxl_list = Object.keys(data)
      this.setData({
        classrooms: data,
        selecter: [jxl_list.map(v => Object({ text: v })), []]
      })
    })

    this.setData({
      dialog_buttons: [{
        text: "关闭",
        tap: () => this.setData({ dialog: {} })
      }]
    })

    if (options.page == 'overview') {
      let { jxlmc, jsmph } = options
      this.switchClassroom(jxlmc, jsmph)
    }
  },

  onShow(): void {
    this.setData({ dqjc: getJc(new Date()) })
    wx.getStorage({
      key: 'last_overview',
      success: res => {
        let { jxlmc, jsmph } = res.data
        this.switchClassroom(jxlmc, jsmph)
      },
      fail: () => this.onPickerChange({ detail: { column: 0, value: 0 } })
    })
  },

  switchClassroom(jxlmc: string, jsmph: string) {
    let selecter = this.data.selecter
    this.onPickerChange({
      detail: {
        column: 0,
        value: selecter[0].findIndex(item => item.text == jxlmc)
      }
    })
    selecter = this.data.selecter
    this.onPickerChange({
      detail: {
        column: 1,
        value: selecter[1].findIndex(item => item.text == jsmph)
      }
    })
  },

  onPickerChange(e: any) {
    const selecter = this.data.selecter
    const selected = this.data.selected
    const { column, value } = e.detail
    selected[column] = value
    if (column == 0) {
      selected[1] = 0
      const jxl_name = selecter[0][value].text
      selecter[1] = this.data.classrooms[jxl_name].map((v: any) => {
        v.text = v.JSMPH
        return v
      })
    }
    this.setData({ selecter, selected })
    this.submit()
    wx.setStorage({
      key: 'last_overview',
      data: {
        jxlmc: selecter[0][selected[0]].text,
        jsmph: selecter[1][selected[1]].text,
      }
    })
  },

  /**
   * 前一个教室
   */
  bindFormer(): void {
    this.onPickerChange({
      detail: {
        column: 1,
        value: (this.data.selected[1] + this.data.selecter[1].length - 1) % (this.data.selecter[1].length)
      }
    })
  },
  /**
   * 后一个教室
   */
  bindLatter(): void {
    this.onPickerChange({
      detail: {
        column: 1,
        value: (this.data.selected[1] + 1) % (this.data.selecter[1].length)
      }
    })
  },

  submit() {
    const selecter = this.data.selecter
    const selected = this.data.selected
    const jasdm = selecter[1][selected[1]].JASDM
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
          kcmclimit = (this.data.cellHeight * (bar_list[i].jc_js - bar_list[i].jc_ks + 1)) / (this.data.cellWidth * this.data.barRatio / 3 * 1.3) * 3
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
    this.setData({ dialog: item2dialog(item, rq) })
  },

  onShareAppMessage() {
    const selecter = this.data.selecter
    const selected = this.data.selected
    const jxlmc = selecter[1][selected[1]].JXLMC
    const jsmph = selecter[1][selected[1]].JSMPH
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
export { }
