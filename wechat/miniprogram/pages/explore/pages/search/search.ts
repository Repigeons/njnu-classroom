// miniprogram/pages/explore/pages/search/search.js
import { parseKcm } from "../../../../utils/parser"
// 获取应用实例
const app = getApp<IAppOption>()
const perPage = 50

Page({
  /**
   * 页面的初始数据
   */
  data: {
    // 搜索
    keyword: String(),
    showSearch: Boolean(),
    showResult: Boolean(),
    // 筛选
    jxl_array: [{key: '#', value: "不限"}] as Array<KeyValue>,
    jxl_selected: 0,
    rq_array: [
      {key: '#', value: "不限"},
      {key: '1', value: "周一"},
      {key: '2', value: "周二"},
      {key: '3', value: "周三"},
      {key: '4', value: "周四"},
      {key: '5', value: "周五"},
      {key: '6', value: "周六"},
      {key: '0', value: "周日"},
    ],
    rq_selected: 0,
    jc_array: ['第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节', '第11节', '第12节'],
    jc_ks_selected: 0,
    jc_js_selected: 11,
    zylxdm_array: Array<KeyValue>(),
    zylxdm_selected: 0
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (/*options*/) {
    app.getClassrooms().then(data => {
      let jxl_array = this.data.jxl_array
      Object.keys(data).forEach(jxlmc => {
        jxl_array.push({ key: jxlmc, value: jxlmc })
      })
      this.setData({ jxl_array })
    })
    app.getZylxdm().then(zylxdm_array => this.setData({ zylxdm_array }))
  },

  onFocus(): void {
    this.setData({
      showSearch: true,
      showResult: false,
    })
  },

  onInput(e: any) {
    this.setData({ keyword: e.detail.value })
  },

  bindRqChange(e: any) {
    this.setData({ rq_selected: e.detail.value })
  },
  bindJxlChange(e: any) {
    this.setData({ jxl_selected: e.detail.value })
  },
  bindJcChange(e: any) {
    let data: Record<string, string> = {}
    data[`jc_${e.target.dataset.jc}_selected`] = e.detail.value
    this.setData(data)

    let {jc_ks_selected, jc_js_selected} = this.data
    if (jc_ks_selected > jc_js_selected) {
      this.setData({
        jc_ks_selected: jc_js_selected,
        jc_js_selected: jc_ks_selected,
      })
    }
  },
  bindZylxChange(e: any) {
    this.setData({ zylxdm_selected: e.detail.value })
  },

  onSearch() {
    this.setData({ showSearch: false })
    if (this.data.keyword) {
      wx.request({
        url: `${app.globalData.server}/api/searchmore.json`,
        data:{
          day: this.data.rq_array[this.data.rq_selected].key,
          jc_ks: this.data.jc_ks_selected + 1,
          jc_js: this.data.jc_js_selected + 1,
          jxl: this.data.jxl_array[this.data.jxl_selected].key,
          zylxdm: this.data.zylxdm_array[this.data.zylxdm_selected].key,
          kcm: this.data.keyword
        },
        success: res => {
          let resData = res.data as Record<string,any>
          let data = resData.data as Array<IClassroomRow>
          for (let i = 0; i < data.length; i++) {
            let info = parseKcm(data[i].zylxdm, data[i].kcm)
            if (info == null) continue
            for (let k in info)
              data[i][k] = info[k]
            data[i].dayIndex = data[i].day + 1
          }
          this.setData({
            service: resData.service,
            search_result: data,
            result_size: data.length,
            display_list: data.slice(0, perPage),
            showResult: true,
          })
        },
        fail: res => {
          console.error(res)
          this.setData({ display_list: [] })
        }
      })
    }

    this.setData({
      showSearch: false,
      showResult: true,
    })
    wx.showToast({ title: `搜索关键词：`+this.data.keyword })
  },

  onShareAppMessage() {
    return {
      title: '更多搜索',
      path: 'pages/explore/pages/search/search'
      // + `?page=search`
      // + `&keyword=${this.data.keyword}`
      // + `&rq_selected=${this.data.rq_selected}`
      // + `&jc_ks_selected=${this.data.jc_ks_selected}`
      // + `&jc_js_selected=${this.data.jc_js_selected}`
      // + `&jxl_selected=${this.data.jxl_selected}`
      // + `&lx_selected=${this.data.lx_selected}`
      // + `&showSearch=${this.data.showSearch}`,
      // image: 'images/logo.png'
    }
  }
})
export {}
