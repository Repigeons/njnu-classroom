// empty.ts
// 获取应用实例
const app = getApp<IAppOption>()
import { getDistance, getJc } from '../../utils/util'

Page({
  data: {
    // 公告
    notice: {} as INotice,
    DoNotShowButton: [{text: "不再显示"}],
    // 筛选
    jxl_array: {} as Array<IPosition>,
    jxl_selected: 0,
    jxl_scroll: 0,
    rq_array: [
      {key: '1', value: "周一"},
      {key: '2', value: "周二"},
      {key: '3', value: "周三"},
      {key: '4', value: "周四"},
      {key: '5', value: "周五"},
      {key: '6', value: "周六"},
      {key: '0', value: "周日"},
    ] as Array<KeyValue>,
    rq_selected: 0,
    rq_scroll: 0,
    jc_array: ['第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节', '第11节', '第12节'],
    jc_selected: 0,
    jc_scroll: 0,
    // 结果
    serve: true,
    result: Array(),
    // 反馈
    layer_index: 0,
    layer_display: false,
    confirm_display: false,
    layer_buttons: Array<ILayerButton>(),
    confirm_buttons: Array<ILayerButton>(),
    feedbackTime: 0,
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名（仅用于列表显示）
   */
  onLoad(options: Record<string, string>): void {
    // 公告
    app.getNotice().then(data => {
      let notice = wx.getStorageSync('notice') as number
      this.setData({
        notice: {
          timestamp: (data.timestamp==notice) ? 0 : data.timestamp,
          date: data.date,
          text: data.text
        }
      })
    })

    // 加载教学楼位置
    app.getJxlPosition().then(data => {
      this.setData({ jxl_array: data })
      // 初始化至当前状态
      this.dangqianriqi()
      this.dangqianjieci()
      this.dingwei()
    })

    // 上报错误
    this.setData({
      layer_buttons: [{
        text: '提交错误',
        tap: () => this.setData({
          layer_display: false,
          confirm_display: true,
        })
      }],
      confirm_buttons: [{
        text: '提交',
        tap: this.feedback
      }, {
        text: '取消',
        tap: () => this.setData({ confirm_display: false })
      }]
    })

    if (options.page == 'empty') {
    }
  },

  /**
   * 生命周期函数--监听页面显示
   * 每次显示时重置状态
   */
  onShow(): void {
    this.hideLayer()
  },

  /**
   * 获取当前定位并选择最近的教学楼
   */
  dingwei(): void {
    wx.getLocation({
      type: 'gcj02',
      success: res => {
        let minId: number = 0
        let minDistance: number = 0xffffffff
        for (let jxlIndex = 0; jxlIndex < this.data.jxl_array.length; jxlIndex++) {
          let distance: number = getDistance({
            latitude1: this.data.jxl_array[jxlIndex].positon[0],
            longitude1: this.data.jxl_array[jxlIndex].positon[1],
            longitude2: res.longitude,
            latitude2: res.latitude,
          })
          if (minDistance > distance) {
            minDistance = distance
            minId = jxlIndex
          }
        }
        this.setData({
          jxl_selected: minId,
          jxl_scroll: minId,
        })
        this.submit()
      },
      fail: console.error
    })
  },
  /**
   * 将选择的日期设为当天
   */
  dangqianriqi(): void {
    let rq = (new Date().getDay() + 6) % 7
    this.setData({
      rq_selected: rq,
      rq_scroll: rq,
    })
    this.submit()
  },
  /**
   * 将选择的课程节次设为当前节次
   */
  dangqianjieci(): void {
    let jc = getJc(new Date())
    this.setData({
      jc_selected: jc,
      jc_scroll: jc,
    })
    this.submit()
  },

  /**
   * 选择教学楼
   */
  bindJxlChange(e: any): void {
    this.setData({ jxl_selected: +e.detail.value })
    this.submit()
  },
  /**
   * 选择日期
   */
  bindRqChange(e: any): void {
    this.setData({ rq_selected: +e.detail.value })
    this.submit()
  },
  /**
   * 选择节次
   */
  bindJcChange(e: any): void {
    this.setData({ jc_selected: +e.detail.value })
    this.submit()
  },

  /**
   * 提交请求至服务器，更新显示的数据
   */
  submit(): void {
    wx.request({
      url: `${app.globalData.server}/api/empty.json`,
      data: {
        day: this.data.rq_array[this.data.rq_selected].key,
        jxl: this.data.jxl_array[this.data.jxl_selected].name,
        dqjc: this.data.jc_selected + 1
      },
      success: res => {
        let resData = res.data as Record<string,any>
        this.setData({
          serve: resData.service == 'on',
          result: resData.data
        })
      },
      fail: err => {
        console.error(err)
        this.setData({ result: [] })
      }
    })
  },

  /**
   * 
   */
  feedback(): void {
    this.setData({ confirm_display: false })
    const interval: number = 60000 // 间隔时间（毫秒）
    let now: number = new Date().getTime()
    if (now < this.data.feedbackTime + interval) {
      wx.showToast({
        title: '操作过于频繁',
        icon: 'loading',
        duration: 500
      })
      return
    }
    wx.showToast({
      title: '发送中',
      icon: 'loading'
    })
    wx.request({
      url: `${app.globalData.server}/api/feedback`,
      method: 'POST',
      header: { 'Content-Type': 'application/x-www-form-urlencoded' },
      data: {
          jc: this.data.jc_selected + 1,
          results: JSON.stringify(this.data.result),
          index: this.data.layer_index,
      },
      success: () => {
        wx.hideToast({
          complete: () => wx.showToast({ title: '发送成功' })
        })
        this.setData({
          feedbackTime: new Date().getTime()
        })
      },
      fail: console.error
    })
  },

  /**
   * 显示用户反馈弹出层
   */
  showLayer(e: any): void {
    let index: number = e.currentTarget.dataset.index
    this.setData({
        layer_index: index,
        layer_display: true
    })
  },
  /**
   * 隐藏用户反馈弹出层
   */
  hideLayer(e?: any): void {
    let layer = e?.target.id == 'layer'
    if (!layer) {
      this.setData({
        layer_display: false,
        confirm_display: false,
      })
    }
  },

  /**
   * 关闭公告栏
   */
  DoNotShow(): void {
    wx.setStorage({
      key: 'notice',
      data: this.data.notice.timestamp,
      success: () => this.setData({notice: {timestamp: 0, date: '', text: ''}})
    })
  },

  onShareAppMessage() {
    return {
      title: '空教室查询',
      path: 'pages/empty/empty'
      + `?page=empty`,
      image: 'images/logo.png'
    }
  }
})
export {}
