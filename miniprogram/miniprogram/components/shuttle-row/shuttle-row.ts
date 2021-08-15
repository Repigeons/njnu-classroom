// components/shuttle/shuttle-row/shuttle-row.js
import { parseTime } from "../../utils/parser"

Component({
  /**
   * 组件的属性列表
   */
  properties: {
    time: { type: String },
    from: { type: String },
    to: { type: String },
    via: { type: Boolean },
  },

  /**
   * 组件的初始数据
   */
  data: {
    state: 0,
    deltaTime: 0,
    autoRefresh: 0
  },

  /**
   * 组件的方法列表
   */
  methods: {
    render(): void {
      const now = new Date()
      const deltaTime = parseTime(this.properties.time) - parseTime(`${now.getHours()}:${now.getMinutes()}`)
      if (!this.properties.via) {
        this.setData({ state: 0 })
      } else if (deltaTime <= -15) {
        this.setData({ state: 1, deltaTime: -deltaTime })
      } else if (deltaTime <= 0) {
        this.setData({ state: 2, deltaTime: -deltaTime })
      } else if (deltaTime <= 15) {
        this.setData({ state: 3, deltaTime })
      } else {
        this.setData({ state: 4, deltaTime })
      }
    }
  },
  lifetimes: {
    attached(): void {
      if (!this.data.autoRefresh) {
        this.data.autoRefresh = setInterval(() => this.render(), 30000)
      }
    },
    detached(): void {
      clearInterval(this.data.autoRefresh as number)
      this.data.autoRefresh = 0
    }
  },
  observers: {
    time(): void {
      this.render()
    },
    via(): void {
      this.render()
    }
  }
})
