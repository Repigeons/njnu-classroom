// components/global/searchbar/searchbar.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    inputVal: { type: String },
    focus: { type: Boolean },
    placeholder: {
      type: String,
      value: "搜索"
    },
    buttonText: {
      type: String,
      value: "搜索"
    }
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
    showInput: function () {
      this.triggerEvent('focus')
    },
    clearInput: function () {
      this.triggerEvent('input', { value: "" })
    },
    onInput: function (e) {
      this.triggerEvent('input', e.detail)
    },
    onSearch: function (e) {
        this.triggerEvent('search', e.detail)
    },
  }
})
