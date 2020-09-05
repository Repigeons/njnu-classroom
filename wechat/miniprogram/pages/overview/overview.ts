// index.ts
// 获取应用实例
const app = getApp<IAppOption>()

Page({
  data: {
    cellHeight: 0,
    cellWidth: 0,
    leftBorder: 8,
    topBorder: 56,
    // jc_array: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
    jxl_array: [''],
    jxl_selected: 0,
    js_array: [''],
    js_selected: 0,
  },

  /**
   * 生命周期函数--监听页面加载
   * 生成教学楼名（仅用于列表显示）
   */
  onLoad(): void {
    const { windowHeight, windowWidth } = wx.getSystemInfoSync()
    let cellHeight = (windowHeight - (this.data.topBorder + 20)) / 13
    let cellWidth = (windowWidth - this.data.leftBorder * 2) / 8 - 1
    
    let jxl_array = []
    for (let key in app.globalData.classrooms) {
      jxl_array.push(key)
    }

    this.setData({ cellHeight, cellWidth, jxl_array })
  },

  onShow(): void {
    wx.getStorage({
      key: 'last_overview',
      success: res => {
        let {jxl, js} = res.data
        let jxl_selected = 0, js_selected
        for (let i=0; i<this.data.jxl_array.length; i++) {
          if (this.data.jxl_array[i] == jxl) {
            jxl_selected = i
            break
          }
        }
        let list = app.globalData.classrooms[this.data.jxl_array[jxl_selected]]
        let js_array = []
        for (let i=0; i< list.length; i++) {
          js_array.push(list[i]['JSMPH'])
          if (list[i]['JSMPH'] == js)
            js_selected = i
        }
        this.setData({ jxl_selected, js_array })
        this.bindJsChange({detail:{value:js_selected}})
      },
      fail: () => this.bindJxlChange({detail:{value:2}})
    })
  },

  /**
   * 选择教学楼
   */
  bindJxlChange(e: any): void {
    const jxl_selected = e.detail.value
    let list = app.globalData.classrooms[this.data.jxl_array[jxl_selected]]
    let js_array = []
    for (let i=0; i< list.length; i++) {
      js_array.push(list[i]['JSMPH'])
    }
    this.setData({ jxl_selected, js_array })
    this.bindJsChange({detail:{value:0}})
    wx.setStorage({
      key: 'last_overview',
      data: {
        jxl: this.data.jxl_array[this.data.jxl_selected],
        js: this.data.js_array[this.data.js_selected],
      }
    })
  },

  /**
   * 选择教室
   */
  bindJsChange(e: AnyObject): void {
    const js_selected = e.detail.value
    this.setData({ js_selected })
    wx.setStorage({
      key: 'last_overview',
      data: {
        jxl: this.data.jxl_array[this.data.jxl_selected],
        js: this.data.js_array[this.data.js_selected],
      }
    })
    
    wx.request({
      url: `${app.globalData.server}/api/overview.json`,
      data: {
        jasdm: app.globalData.classrooms[this.data.jxl_array[this.data.jxl_selected]][js_selected]['JASDM']
      },
      success: res => {
        let resData = res.data as Record<string, AnyObject>
        for (let i=0; i<resData.data.length; i++) {
          switch (resData.data[i].zylxdm) {
            case '00':
              resData.data[i].usage = 'empty'
              break;
            case '01':
            case '03':
              resData.data[i].usage = 'class'
              break;
            default:
              resData.data[i].usage = 'others'
              break;
          }
          resData.data[i].day = (+resData.data[i].day + 6) % 7
        }
        this.setData({ bar_list: resData.data })
      }
    })
  },
  logItem(e: AnyObject): void {
    console.log(e.currentTarget.dataset.item)
  }

})
