export { }
import { weekdays2 } from "../../../../utils/constant"
// explore/search
import { getClassrooms, getZylxdm } from "../../../../utils/getCache"
import { request } from "../../../../utils/http"
import { classDetailItem2dialog, parseKcm } from "../../../../utils/parser"

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
    rq_array: weekdays2,
    rq_selected: 0,
    jc_array: ['第1节', '第2节', '第3节', '第4节', '第5节', '第6节', '第7节', '第8节', '第9节', '第10节', '第11节', '第12节'],
    jc_ks_selected: 0,
    jc_js_selected: 11,
    zylxdm_array: Array<KeyValue>(),
    zylxdm_selected: 0,
    // 结果
    serve: true,
    pageNum: 0,
    pageCount: -1,
    totalCount: 0,
    result: Array<IClassroomRow>(),
    dialog: {} as IClassDetailDialog
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    this.preloadInfo()

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

  async preloadInfo() {
    const zylxdm_array = await getZylxdm()
    const classrooms = await getClassrooms()
    const jxl_array = this.data.jxl_array
    Object.keys(classrooms).forEach(jxlmc => {
      jxl_array.push({ key: jxlmc, value: jxlmc })
    })
    this.setData({ zylxdm_array, jxl_array })
  },

  onFocus() {
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

  async submit() {
    this.setData({ showSearch: false })
    if (!this.data.keyword) return
    this.setData({
      pageCount: -1,
      pageNum: 0,
      result: []
    })
    this.requestData()
  },

  async requestData() {
    this.data.pageNum += 1
    if (this.data.pageCount >= 0 && this.data.pageCount < this.data.pageCount)
      return
    const res = await request({
      path: "/api/search.json",
      data: {
        day: this.data.rq_array[this.data.rq_selected].key,
        jcKs: this.data.jc_ks_selected + 1,
        jcJs: this.data.jc_js_selected + 1,
        jxl: this.data.jxl_array[this.data.jxl_selected].key,
        zylxdm: this.data.zylxdm_array[this.data.zylxdm_selected].key,
        kcm: this.data.keyword,
        page: this.data.pageNum
      },
    })
    const result = res.data as IPageResult
    for (let i = 0; i < result.list.length; i++) {
      const info = parseKcm(result.list[i].zylxdm, result.list[i].kcm)
      if (info == null) continue
      for (const k in info)
        result.list[i][k] = info[k]
    }
    this.setData({
      showResult: true,
      serve: res.status == 200,
      totalCount: result.totalCount,
      pageCount: result.pageCount,
      result: this.data.result.concat(result.list)
    })
  },

  onReachBottom() {
    this.requestData()
  },

  /**
    * 显示详细信息
    */
  showDialog(e: any) {
    const index: number = e.currentTarget.dataset.index
    const item = this.data.result[index]
    this.setData({ dialog: classDetailItem2dialog(item, item.day) })
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
