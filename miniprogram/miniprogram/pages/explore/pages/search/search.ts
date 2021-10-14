export { }
// explore/search
import { getClassrooms, getZylxdm } from "../../../../utils/getCache"
import { item2dialog, parseKcm } from "../../../../utils/parser"
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
    jxl_array: [{ key: '#', value: "不限" }] as Array<KeyValue>,
    jxl_selected: 0,
    rq_array: [
      { key: '#', value: "不限" },
      { key: 'Mon.', value: "周一" },
      { key: 'Tue.', value: "周二" },
      { key: 'Wed.', value: "周三" },
      { key: 'Thu.', value: "周四" },
      { key: 'Fri.', value: "周五" },
      { key: 'Sat.', value: "周六" },
      { key: 'Sun.', value: "周日" },
    ],
    rq_selected: 0,
    jc_array: ['第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节', '第11节', '第12节'],
    jc_ks_selected: 0,
    jc_js_selected: 11,
    zylxdm_array: Array<KeyValue>(),
    zylxdm_selected: 0,
    // 结果
    serve: true,
    result: Array<IClassroomRow>(),
    results: Array<IClassroomRow>(),
    dialog: {},
    dialog_buttons: Array<IButton>(),
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    getClassrooms().then(data => {
      const jxl_array = this.data.jxl_array
      Object.keys(data).forEach(jxlmc => {
        jxl_array.push({ key: jxlmc, value: jxlmc })
      })
      this.setData({ jxl_array })
    })
    getZylxdm().then(zylxdm_array => this.setData({ zylxdm_array }))

    this.setData({
      dialog_buttons: [{
        text: "关闭",
        tap: () => this.setData({ dialog: {} })
      }]
    })

    if (options.page === "search") {
      const { keyword, jxl_selected, rq_selected, jc_ks_selected, jc_js_selected, zylxdm_selected } = options
      this.setData({
        keyword,
        jxl_selected: Number(jxl_selected),
        rq_selected: Number(rq_selected),
        jc_ks_selected: Number(jc_ks_selected),
        jc_js_selected: Number(jc_js_selected),
        zylxdm_selected: Number(zylxdm_selected),
      })
      this.submit()
    }
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
    const data: Record<string, string> = {}
    data[`jc_${e.target.dataset.jc}_selected`] = e.detail.value
    this.setData(data)

    const { jc_ks_selected, jc_js_selected } = this.data
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

  submit() {
    this.setData({ showSearch: false })
    if (this.data.keyword) {
      wx.request({
        url: `${app.globalData.server}/api/search.json`,
        data: {
          day: this.data.rq_array[this.data.rq_selected].key,
          jc_ks: this.data.jc_ks_selected + 1,
          jc_js: this.data.jc_js_selected + 1,
          jxl: this.data.jxl_array[this.data.jxl_selected].key,
          zylxdm: this.data.zylxdm_array[this.data.zylxdm_selected].key,
          kcm: this.data.keyword
        },
        success: res => {
          const data = res.data as IJsonResponse
          if (res.statusCode == 200 || res.statusCode == 418) {
            const rows = data.data as Array<IClassroomRow>
            for (let i = 0; i < rows.length; i++) {
              const info = parseKcm(rows[i].zylxdm, rows[i].kcm)
              if (info == null) continue
              for (const k in info)
                rows[i][k] = info[k]
            }
            this.setData({
              serve: data.status == 200,
              results: rows,
              result: rows.slice(0, perPage),
              showResult: true,
            })
          } else {
            console.warn(data.message)
            this.setData({ display_list: [] })
          }
        },
        fail: res => {
          console.error(res)
          this.setData({ display_list: [] })
        }
      })
    }
  },

  onReachBottom() {
    const { result, results } = this.data
    this.setData({
      result: result.concat(results.slice(result.length, result.length + perPage))
    })
  },

  /**
    * 显示详细信息
    */
  showDialog(e: any): void {
    const index: number = e.currentTarget.dataset.index,
      item = this.data.result[index],
      rq = this.data.rq_array[item.day ? item.day : 7].value
    this.setData({ dialog: item2dialog(item, rq) })
  },

  onShareAppMessage() {
    return {
      title: '更多搜索',
      path: 'pages/explore/pages/search/search'
        + `?page=search`
        + `&keyword=${this.data.keyword}`
        + `&jxl_selected=${this.data.jxl_selected}`
        + `&rq_selected=${this.data.rq_selected}`
        + `&jc_ks_selected=${this.data.jc_ks_selected}`
        + `&jc_js_selected=${this.data.jc_js_selected}`
        + `&zylxdm_selected=${this.data.zylxdm_selected}`,
      image: 'images/logo.png'
    }
  }
})
