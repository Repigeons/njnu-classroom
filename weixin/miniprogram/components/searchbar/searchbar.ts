// components/global/searchbar/searchbar.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    focus: { type: Boolean },
    value: { type: String },
    placeholder: {
      type: String,
      value: "搜索"
    },
    buttonText: {
      type: String,
      value: "搜索"
    },
  },

  /**
   * 组件的初始数据
   */
  data: {
  },

  /**
   * 组件的方法列表
   */
  methods: {
    onFocus() {
      if (!this.properties.focus) this.triggerEvent('focus')
    },
    clearInput() {
      this.triggerEvent('input', { value: "" })
    },
    onInput(e) {
      this.triggerEvent('input', e.detail)
    },
    onSearch(e) {
        this.triggerEvent('search', e.detail)
    },
  }
})
