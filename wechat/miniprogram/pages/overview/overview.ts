// index.ts
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
    dqxq: new Date().getDay(),
    time_array: [
      ['08:00', '08:40'], ['08:45', '09:25'], ['09:40', '10:20'], ['10:35', '11:15'], ['11:20', '12:00'],
      ['13:30', '14:10'], ['14:15', '14:55'], ['15:10', '15:50'], ['15:55', '16:35'],
      ['18:30', '19:10'], ['19:20', '20:00'], ['20:10', '20:50'],
    ],
    jxl_array: [''],
    jxl_selected: 0,
    js_array: [''],
    js_selected: 0,
    dialog: {},
    bar_list: Array<IClassroomRow>(),
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名（仅用于列表显示）
   */
  onLoad(): void {
    console.log(new Date().getDay())
    const { windowHeight, windowWidth } = wx.getSystemInfoSync()
    let cellHeight = (windowHeight - (this.data.topBorder + 20)) / 13
    let cellWidth = (windowWidth - this.data.leftBorder * 2) / 8 - 1
    
    let jxl_array = []
    for (let key in app.globalData.classrooms) {
      jxl_array.push(key)
    }

    this.setData({ cellHeight, cellWidth, jxl_array })
  },

  onShow(): void {
    this.setData({ dqjc: getJc(new Date()) })
    wx.getStorage({
      key: 'last_overview',
      success: res => {
        let {jxl, js} = res.data
        let jxl_selected = 0, js_selected
        for (let i=0; i<this.data.jxl_array.length; i++) {
          if (this.data.jxl_array[i] == jxl) {
            jxl_selected = i
            break
          }
        }
        let list = app.globalData.classrooms[this.data.jxl_array[jxl_selected]]
        let js_array = []
        for (let i=0; i< list.length; i++) {
          js_array.push(list[i]['JSMPH'])
          if (list[i]['JSMPH'] == js)
            js_selected = i
        }
        this.setData({ jxl_selected, js_array })
        this.bindJsChange({detail:{value:js_selected}})
      },
      fail: () => this.bindJxlChange({detail:{value:2}})
    })
  },

  /**
   * 选择教学楼
   */
  bindJxlChange(e: any): void {
    const jxl_selected = e.detail.value
    let list = app.globalData.classrooms[this.data.jxl_array[jxl_selected]]
    let js_array = []
    for (let i=0; i< list.length; i++) {
      js_array.push(list[i]['JSMPH'])
    }
    this.setData({ jxl_selected, js_array })
    this.bindJsChange({detail:{value:0}})
    wx.setStorage({
      key: 'last_overview',
      data: {
        jxl: this.data.jxl_array[this.data.jxl_selected],
        js: this.data.js_array[this.data.js_selected],
      }
    })
  },

  /**
   * 选择教室
   */
  bindJsChange(e: AnyObject): void {
    const js_selected = e.detail.value
    this.setData({ js_selected })
    wx.setStorage({
      key: 'last_overview',
      data: {
        jxl: this.data.jxl_array[this.data.jxl_selected],
        js: this.data.js_array[this.data.js_selected],
      }
    })
    
    wx.request({
      url: `${app.globalData.server}/api/overview.json`,
      data: {
        jasdm: app.globalData.classrooms[this.data.jxl_array[this.data.jxl_selected]][js_selected]['JASDM']
      },
      success: res => {
        let resData = res.data as Record<string, AnyObject>
        let data = resData.data as Array<IClassroomRow>
        let kcmclimit = 0
        for (let i = 0; i < data.length; i++) {
          switch (data[i].zylxdm) {
            case '00':
              data[i].usage = 'empty'
              break;
            case '01':
            case '03':
            case '10':
            case '11':
              data[i].usage = 'class'
              break;
            default:
              data[i].usage = 'others'
              break;
          }
          data[i].day2 = `${+data[i].day + 1}`
          data[i].day = `${(+data[i].day + 6) % 7}`
          let info = parseKcm(data[i].zylxdm, data[i].kcm)
          if (info == null) continue
          for (let k in info)
            data[i][k] = info[k]
          kcmclimit=(this.data.cellHeight * (parseInt(data[i].jc_js) - parseInt(data[i].jc_ks) + 1)) / (this.data.cellWidth * this.data.barRatio/3*1.3) * 3
          data[i].shortkcmc= data[i].title.length > kcmclimit ? data[i].title.substring(0, kcmclimit - 3) + '...' : data[i].title
        }
        this.setData({ bar_list: data })
        //console.log(resData.data)
      }
    })
  },

  bindFormer(): void {
    let value = (this.data.js_selected - 1 + this.data.js_array.length) % this.data.js_array.length
    this.bindJsChange({detail:{value}})
  },

  bindLatter(): void {
    let value = (this.data.js_selected + 1) % this.data.js_array.length
    this.bindJsChange({detail:{value}})
  },

  /**
   * 显示详细信息
   */
  showDialog(e: AnyObject): void {
    const rq_array = ['所有', '周日', '周一', '周二', '周三', '周四', '周五', '周六']
    const index: number = e.currentTarget.dataset.index
    const item = this.data.bar_list[index]
    const rq: string = rq_array[+item.day2]
    this.setData({dialog: item2dialog(item, rq)})
    //console.log((this.data.cellHeight*(parseInt(item.jc_js)-parseInt(item.jc_ks)+1))/(this.data.cellWidth*0.45-3))
  },

  closeDialog(): void {
    this.setData({dialog: {}})
  },
})