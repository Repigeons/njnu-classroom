// miniprogram/pages/explore/pages/search/search.js
Page({
  /**
   * 页面的初始数据
   */
  data: {
    keyword: String(),
    showSearch: Boolean(),
    showResult: Boolean(),
    selected: 0,
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (/*options*/) {

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

  onSearch() {
    this.setData({
      showSearch: false,
      showResult: true,
    })
    wx.showToast({ title: `搜索关键词：`+this.data.keyword })
  },

  onSelect(e: any) {
    this.setData({ selected: e.detail.value })
  },

  onButton(e: any) {
    console.log(e)
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
