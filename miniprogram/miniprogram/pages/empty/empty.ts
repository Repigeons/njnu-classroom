export { }
// empty
import { getJxlPosition } from '../../utils/getCache'
import { getDistance, getJc } from '../../utils/util'
import { request } from '../../utils/http'
import { weekdays } from '../../utils/constant'

const feedbackInterval: number = 5000 // 间隔时间（毫秒）

Page({
  data: {
    // 筛选
    jxl_array: {} as Array<IPosition>,
    jxl_selected: 0,
    jxl_scroll: 0,
    rq_array: weekdays,
    rq_selected: 0,
    rq_scroll: 0,
    jc_selected: 0,
    jc_scroll: 0,
    // 结果
    serve: true,
    result: Array<IClassroomRow>(),
    // 反馈
    layer_index: 0,
    layer_display: false,
    confirm_display: false,
    layer_buttons: Array<IButton>(),
    confirm_buttons: Array<IButton>(),
    feedbackTime: 0,
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名（仅用于列表显示）
   */
  onLoad(options: Record<string, string>) {
    this.preloadInfo()
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
      }],
    })

    if (options.page == 'empty') {
      // always true
    }
  },

  async preloadInfo() {
    // 加载教学楼位置
    const jxl_array = await getJxlPosition()
    console.debug(jxl_array)
    this.setData({ jxl_array })
    // 初始化至当前状态
    this.dangqianriqi()
    this.dangqianjieci()
    this.dingwei()
  },

  /**
   * 生命周期函数--监听页面显示
   * 每次显示时重置状态
   */
  onShow() {
    this.hideLayer()
  },

  /**
   * 获取当前定位并选择最近的教学楼
   */
  async dingwei() {
    const res: WechatMiniprogram.GetLocationSuccessCallbackResult = await wx.getLocation({
      type: 'gcj02'
    }) as any as WechatMiniprogram.GetLocationSuccessCallbackResult
    console.debug('location', res)
    let minIndex: number = 0
    let minDistance: number = 0xffffffff
    this.data.jxl_array.forEach((jxl, index) => {
      const distance: number = getDistance({
        latitude1: jxl.position[0],
        longitude1: jxl.position[1],
        longitude2: res.longitude,
        latitude2: res.latitude,
      })
      if (minDistance > distance) {
        minDistance = distance
        minIndex = index
      }
    })
    this.setData({
      jxl_selected: minIndex,
      jxl_scroll: minIndex,
    })
    this.submit()
  },
  /**
   * 将选择的日期设为当天
   */
  dangqianriqi() {
    const rq = (new Date().getDay() + 6) % 7
    this.setData({
      rq_selected: rq,
      rq_scroll: rq,
    })
    this.submit()
  },
  /**
   * 将选择的课程节次设为当前节次
   */
  dangqianjieci() {
    const jc = getJc(new Date())
    this.setData({
      jc_selected: jc,
      jc_scroll: jc,
    })
    this.submit()
  },

  /**
   * 选择教学楼
   */
  bindJxlChange(e: any) {
    this.setData({ jxl_selected: +e.detail.value })
    this.submit()
  },
  /**
   * 选择日期
   */
  bindRqChange(e: any) {
    this.setData({ rq_selected: +e.detail.value })
    this.submit()
  },
  /**
   * 选择节次
   */
  bindJcChange(e: any) {
    this.setData({ jc_selected: +e.detail.value })
    this.submit()
  },

  /**
   * 提交请求至服务器，更新显示的数据
   */
  async submit() {
    const res = await request({
      path: "/api/empty.json",
      data: {
        day: this.data.rq_array[this.data.rq_selected].key,
        jxl: this.data.jxl_array[this.data.jxl_selected].name,
        jc: this.data.jc_selected + 1
      }
    })
    console.debug("empty.json", res)
    this.setData({
      serve: res.status == 200,
      result: res.data as Array<IClassroomRow>
    })
  },

  /**
   *
   */
  async feedback() {
    this.setData({ confirm_display: false })
    const rq = (new Date().getDay() + 6) % 7
    const jc = getJc(new Date())
    if (this.data.rq_selected != rq || this.data.jc_selected != jc) {
      wx.showToast({
        title: '未选择当前星期或节次',
        icon: 'none'
      })
      this.dangqianriqi()
      this.dangqianjieci()
      return
    }

    const now: number = new Date().getTime()
    if (now < this.data.feedbackTime + feedbackInterval) {
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
    await request({
      path: "/api/empty/feedback",
      method: "POST",
      data: {
        jc: this.data.jc_selected + 1,
        results: this.data.result,
        index: this.data.layer_index,
        day: this.data.rq_array[this.data.rq_selected].key,
        jxl: this.data.jxl_array[this.data.jxl_selected].name,
      }
    })
    wx.hideToast({
      complete() {
        wx.showToast({
          title: '发送成功',
          icon: 'success'
        })
      }
    })
    this.setData({
      feedbackTime: new Date().getTime()
    })
  },

  /**
   * 显示用户反馈弹出层
   */
  showLayer(e: any) {
    const index: number = e.currentTarget.dataset.index
    this.setData({
      layer_index: index,
      layer_display: true
    })
  },
  /**
   * 隐藏用户反馈弹出层
   */
  hideLayer(e?: any) {
    const layer = e?.target.id == 'layer'
    if (!layer) {
      this.setData({
        layer_display: false,
        confirm_display: false,
      })
    }
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
