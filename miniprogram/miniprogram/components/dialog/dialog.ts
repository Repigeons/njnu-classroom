// components/dialog/dialog.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    show: { type: Boolean },
    title: { type: String },
    buttons: { type: Array }
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
    onClose() {
      this.setData({ show: false })
    },
    onButton(e) {
      const index = +e.target.dataset.index
      const button = this.properties.buttons[index]
      if (typeof button.tap == 'function') {
        button.tap(e)
      } else {
        console.warn(`Button ["${button.text}"] does not have a method on handler "tap"`)
      }
    }
  }
})
