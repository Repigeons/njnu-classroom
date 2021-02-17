// components/layer.ts

interface ILayerButton {
  text: string,
  tap?: (e:any) => any,
  longpress?: (e:any) => any,
}

Component({
  /**
   * 组件的属性列表
   */
  properties: {
    buttons: {
      type: Array,
      value: []
    },
    BackColor: {
      type: String,
      value: '#000'
    },
    ForeColor: {
      type: String,
      value: '#fff'
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
    tap(e): void {
      const index = e.target.dataset.button_index
      if (this.properties.buttons[index].tap)
        this.properties.buttons[index].tap(e)
    },
    longpress(e): void {
      const index = e.target.dataset.button_index
      if (this.properties.buttons[index].longpress)
        this.properties.buttons[index].longpress(e)
    },
  }
})
