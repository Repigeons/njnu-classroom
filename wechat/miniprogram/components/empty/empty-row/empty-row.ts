// components/empty-classroom/empty-classroom.js
Component({
  /**
   * 组件的属性列表
   */
  properties: {
    zylxdm: { type: String },
    jsmph: { type: String },
    jc_ks: { type: Number },
    jc_js: { type: Number },
    skzws: { type: Number },
  },

  /**
   * 组件的初始数据
   */
  data: {
    icon: {
      '00': "kong.png",
      '01': "benke.png",
      '03': "benke.png",
      '02': "jieyong.png",
      '04': "jieyong.png",
      '05': "qita.png",
      '10': "yanjiusheng.png",
      '11': "yanjiusheng.png",
    }
  },

  /**
   * 组件的方法列表
   */
  methods: {

  }
})
