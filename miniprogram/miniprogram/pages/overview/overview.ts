export { }
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
    jxl_list: Array<IJasInfo>(),
    jxl_picker_selected: 0,
    jxl_display_selected: 0,
    jas_picker_list: Array<IJasInfo>(),
    jas_picker_selected: 0,
    jas_display_list: Array<IJasInfo>(),
    jas_display_selected: 0,
    // 布局
    cellHeight: 0,
    cellWidth: 0,
    leftBorder: 8,
    topBorder: 56,
    barRatio: 0.8,
    dqjc: 1,
    // 周日->0
    today: new Date().getDay(),
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
    const cellHeight = (windowHeight - (this.data.topBorder + 20 + 2)) / 13
    const cellWidth = (windowWidth - (this.data.leftBorder * 2 + 2)) / 8 - 1
    this.setData({ cellHeight, cellWidth })

    getClassrooms().then(data => {
      this.setData({
        classrooms: data,
        jxl_list: Object.keys(data).map(v => Object({ text: v }))
      })
    })

    this.setData({
      dialog_buttons: [{
        text: "关闭",
        tap: () => this.setData({ dialog: {} })
      }]
    })

    if (options.page == 'overview') {
      const { jxlmc, jsmph } = options
      this.switchClassroom(jxlmc, jsmph)
    }
  },

  onShow(): void {
    this.setData({ dqjc: getJc(new Date()) })
    wx.getStorage({
      key: 'last_overview',
      success: res => {
        const { jxlmc, jsmph } = res.data
        this.switchClassroom(jxlmc, jsmph)
      },
      fail: () => {
        this.onPickerChange({ detail: { column: 0, value: 0 } })
        this.onSubmit()
      }
    })
  },

  switchClassroom(jxlmc: string, jsmph: string) {
    const jxl_list = this.data.jxl_list
    this.onPickerChange({
      detail: {
        column: 0,
        value: jxl_list.findIndex(item => item.text == jxlmc)
      }
    })
    const jas_picker_list = this.data.jas_picker_list
    this.onPickerChange({
      detail: {
        column: 1,
        value: jas_picker_list.findIndex(item => item.text == jsmph)
      }
    })
    this.onSubmit()
  },

  onPickerChange(e: any) {
    const { column, value } = e.detail
    if (column == 0) {
      const jxl_name = this.data.jxl_list[value].text
      const jas_picker_list = this.data.classrooms[jxl_name].map(v => {
        v.text = v.JSMPH
        return v
      })
      this.setData({
        jxl_picker_selected: value,
        jas_picker_list,
        jas_picker_selected: 0
      })
    } else {
      this.setData({ jas_picker_selected: value })
    }
  },

  /**
   * 前一个教室
   */
  bindFormer(): void {
    this.onPickerChange({
      detail: {
        column: 1,
        value: (this.data.jas_picker_selected + this.data.jas_picker_list.length - 1) % (this.data.jas_picker_list.length)
      }
    })
    this.onSubmit()
  },
  /**
   * 后一个教室
   */
  bindLatter(): void {
    this.onPickerChange({
      detail: {
        column: 1,
        value: (this.data.jas_picker_selected + 1) % (this.data.jas_picker_list.length)
      }
    })
    this.onSubmit()
  },

  onPickerCancel() {
    this.setData({
      jxl_picker_selected: this.data.jxl_display_selected,
      jas_picker_list: this.data.jas_display_list,
      jas_picker_selected: this.data.jas_display_selected
    })
  },

  onSubmit() {
    this.setData({
      jxl_display_selected: this.data.jxl_picker_selected,
      jas_display_list: this.data.jas_picker_list,
      jas_display_selected: this.data.jas_picker_selected
    })
    const jas = this.data.jas_display_list[this.data.jas_display_selected]
    const jxlmc = jas.JXLMC
    const jsmph = jas.JSMPH
    const jasdm = jas.JASDM
    wx.setStorage({
      key: 'last_overview',
      data: { jxlmc, jsmph }
    })
    wx.request({
      url: `${app.globalData.server}/api/overview.json`,
      data: { jasdm },
      success: res => {
        const data = res.data as IJsonResponse
        if (res.statusCode == 200) {
          const bar_list = data.data as Array<IClassroomRow>
          let kcmclimit = 0
          const dayMapper: Record<string, number> = {
            'Mon.': 0,
            'Tue.': 1,
            'Wed.': 2,
            'Thu.': 3,
            'Fri.': 4,
            'Sat.': 5,
            'Sun.': 6,
          }
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
            if (dayMapper[bar_list[i].day] + 1 == this.data.today)
              if (bar_list[i].jc_ks <= this.data.dqjc + 1)
                if (bar_list[i].jc_js >= this.data.dqjc + 1) {
                  this.setData({ empty: bar_list[i].zylxdm == '00' })
                }
            bar_list[i].left = dayMapper[bar_list[i].day]
            const info = parseKcm(bar_list[i].zylxdm, bar_list[i].kcm)
            if (info == null) continue
            for (const k in info) {
              bar_list[i][k] = info[k]
            }
            kcmclimit = (this.data.cellHeight * (bar_list[i].jc_js - bar_list[i].jc_ks + 1)) / (this.data.cellWidth * this.data.barRatio / 3 * 1.3) * 3
            bar_list[i].shortkcmc = bar_list[i].title.length > kcmclimit ? bar_list[i].title.substring(0, kcmclimit - 3) + '...' : bar_list[i].title
          }
          this.setData({ bar_list })
        } else {
          console.warn(data.message)
          this.setData({ bar_list: [] })
        }
      },
      fail: console.error
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
    const jas = this.data.jas_display_list[this.data.jas_display_selected]
    const jxlmc = jas.JXLMC
    const jsmph = jas.JSMPH
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
