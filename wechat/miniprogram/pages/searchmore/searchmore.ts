// searchmore.ts
// 获取应用实例
const app = getApp<IAppOption>()
import { parseKcm, item2dialog } from '../../utils/parser'
import { IClassroomRow } from '../../../typings/IClassroomInfo'

// constant
const jxl: Array<IJxl> = app.globalData.jxl
const lx: Array<ILx> = app.globalData.lx
const perPage: number = 50

Page({
  data: {
    service: 'on',
    // 筛选
    rq_array: ['所有', '周日', '周一', '周二', '周三', '周四', '周五', '周六'],
    rq_selected: 0,

    jc_array: ['第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节', '第11节', '第12节'],
    jc_js_array: new Array<string>(), jc_ks_array: new Array<string>(),
    jc_ks_selected: 0, jc_js_selected: 11,
    
    jxl_name_array: new Array<string>(),
    jxl_selected: 0,
    
    lx_name_array: new Array<string>(),
    lx_selected: 0,

    keyword: '',
    showInput: false,
    showButton: false,
    showResult: false,

    // 结果集
    iconPath: {
      '01': '/images/benke.png',
      '03': '/images/benke.png',
      '02': '/images/jieyong.png',
      '04': '/images/jieyong.png',
      '05': '/images/qita.png',
      '10': '/images/yanjiusheng.png',
      '11': '/images/yanjiusheng.png',
    },
    dialog: {},
    list: Array<IClassroomRow>(),
    result_size: new Number()
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名、类型吗（仅用于列表显示）
   * 初始化可选节次数组
   */
  onLoad(): void {
    const jxl_name_array: Array<string> = ['所有']
    const lx_name_array: Array<string> = []
    for (let i = 0; i < jxl.length; i++)
      jxl_name_array.push(jxl[i].name)
    for (let i = 0; i < lx.length; i++)
      lx_name_array.push(lx[i].name)
    this.setData({jxl_name_array, lx_name_array})

    this.updateJcArray()
  },

  /**
   * 更新节次列表
   */
  updateJcArray(): void {
    const jc_ks_array: Array<string> = []
    const jc_js_array: Array<string> = []
    for (let i = 0; i <= this.data.jc_js_selected; i++)
      jc_ks_array.push(this.data.jc_array[i])
    for (let i = this.data.jc_ks_selected; i < 12; i++)
      jc_js_array.push(this.data.jc_array[i])
    this.setData({jc_ks_array, jc_js_array})
  },

  /**
   * 显示输入框
   */
  showInput(): void {
    this.setData({
      showInput: true,
      showButton: true,
      showResult: false
    })
  },

  /**
   * 显示按钮
   */
  showButton(): void {
    this.setData({
      showButton: true,
      showResult: false
    })
  },

  /**
   * 搜索
   */
  onSearch(): void {
    this.setData({ showButton: false })
    if (this.data.keyword) {
      wx.request({
        url: `${app.globalData.server}/searchmore.json`,
        data:{
          day: (this.data.rq_selected == 0) ? '#' : this.data.rq_selected - 1,
          jc_ks: this.data.jc_ks_selected + 1,
          jc_js: this.data.jc_js_selected + 1,
          jxl: (this.data.jxl_selected == 0) ? '#' : jxl[this.data.jxl_selected].name,
          zylxdm: lx[this.data.lx_selected].dm,
          kcm: this.data.keyword
        },
        success: res => {
          const data = res.data as Array<IClassroomRow>
          for (let i = 0; i < data.length; i++) {
            let info = parseKcm(data[i].zylxdm, data[i].kcm)
            if (info == null) continue
            for (let k in info)
              data[i][k] = info[k]
            data[i].day = `${+data[i].day + 1}`
          }
          this.setData({
            list: data.slice(0, perPage),
            result_size: data.length,
            showResult: true
          })
          wx.setStorage({
            key: 'list',
            data: data
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
  clearInput(): void {
    this.setData({keyword: ''})
  },

  /**
   * 输入搜索关键词
   */
  onInput(e: AnyObject): void {
    this.setData({keyword: e.detail.value.trim()})
  },

  /**
   * 选择日期
   */
  bindRqChange(e: AnyObject): void {
    this.setData({rq_selected: e.detail.value})
  },

  /**
   * 选择开始节次
   */
  bindJcKsChange(e: AnyObject): void {
    this.setData({jc_ks_selected: +e.detail.value})
    this.updateJcArray()
  },

  /**
   * 选择结束节次
   */
  bindJcJsChange(e: AnyObject): void {
    this.setData({jc_js_selected: +e.detail.value + 12 - this.data.jc_js_array.length})
    this.updateJcArray()
  },

  /**
   * 选择教学楼
   */
  bindJxlChange(e: AnyObject): void {
    this.setData({ jxl_selected: +e.detail.value })
  },

  /**
   * 选择类型
   */
  bindLxChange(e: AnyObject): void {
    this.setData({ lx_selected: +e.detail.value })
  },

  onReachBottom(): void {
    wx.getStorage({
      key: 'list',
      success: res => {
        const list = this.data.list as Array<IClassroomRow>
        this.setData({list: list.concat(res.data.slice(list.length, list.length + perPage))})
      }
    })
  },

  /**
   * 显示详细信息
   */
  showDialog(e: AnyObject): void {
    const index: number = e.currentTarget.dataset.index
    const item: IClassroomRow = this.data.list[index]
    const rq: string = this.data.rq_array[+item.day]
    this.setData({dialog: item2dialog(item, rq)})
    // console.log(item)
  },

  closeDialog(): void {
    this.setData({dialog: {}})
  }
})
