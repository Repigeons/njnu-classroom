// components/class-detail/class-detail.ts
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    title: String,
    detail: Object //IClassDetailDialog
  },

  /**
   * 组件的初始数据
   */
  data: {
    dialog_buttons: Array<IButton>()
  },

  /**
   * 组件的方法列表
   */
  methods: {

  },

  lifetimes: {
    attached() {
      this.setData({
        dialog_buttons: [{
          text: "关闭",
          tap: () => this.setData({ title: null, detail: null })
        }]
      })
    }
  }
})
