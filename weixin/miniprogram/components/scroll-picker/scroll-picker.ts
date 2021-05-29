// components/scroll-picker/scroll-picker.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    scroll: { type: Number },
    list: { type: Array },
    key: { type: String },
    selected: { type: Number },

    button: { type: String },
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
    onChange(e) {
      this.triggerEvent('change', { value: +e.currentTarget.dataset.index })
    },
    onButton(e) {
      this.triggerEvent('button', e.detail)
    }
  }
})
