// components/notice/notice.ts
import { request } from "../../utils/http"

Component({
  /**
   * 组件的初始数据
   */
  data: {
    timestamp: Number(),
    date: String(),
    text: String(),
    dialog_buttons: Array<IButton>()
  },

  /**
   * 组件的方法列表
   */
  methods: {
    close() {
      wx.setStorage({
        key: 'notice',
        data: this.data.timestamp,
        success: () => this.setData({ timestamp: 0, date: '', text: '' })
      })
    }
  },
  lifetimes: {
    async attached() {
      this.setData({
        dialog_buttons: [{
          text: '不再显示',
          tap: () => this.close()
        }]
      })
      const res = await request({
        path: "/notice/get"
      })
      const { timestamp, date, text } = res.data
      const notice = wx.getStorageSync('notice') as number
      this.setData({
        timestamp: (timestamp <= notice) ? 0 : timestamp,
        date, text
      })
    }
  }
})