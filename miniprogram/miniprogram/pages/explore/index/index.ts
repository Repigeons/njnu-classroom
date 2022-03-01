export { }
// explore/index
import { getExploreGrids } from "../../../utils/getCache"
import { server } from "../../../utils/http"
let interstitialAd: WechatMiniprogram.InterstitialAd

Page({
  /**
   * 页面的初始数据
   */
  data: {
    fullYear: new Date().getFullYear(),
    grids: Array<IGrid>()
  },

  /**
   * 生命周期函数--监听页面加载
   */
  async onLoad(/*options*/) {
    const data = await getExploreGrids()
    this.setData({ grids: data })
    if (wx.createInterstitialAd) {
      interstitialAd = wx.createInterstitialAd({ adUnitId: 'adunit-cbb4c40d86d77b8b' })
      interstitialAd.onLoad(() => { })
      interstitialAd.onError(console.error)
      interstitialAd.onClose(() => { })
    }
  },

  onTapGrids(e: any) {
    const methods: Record<string, () => void> = {
      developing: () => wx.showToast({ title: "敬请期待", icon: 'none' }),
      calendar: () => wx.previewImage({ urls: [`${server}/images/calendar.jpg`], fail: console.error }),
      support: () => interstitialAd?.show().catch(console.error),
    }
    const method = methods[e.detail.method]
    if (typeof method == "function") method()
  },

  copyQQGroupId() {
    wx.setClipboardData({
      data: '1150057272',
      success: () => wx.showToast({ title: "已复制到剪贴板" })
    })
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage() {
    return {
      title: '发现',
      path: 'pages/explore/explore'
        + `?page=explore`,
      image: "images/logo.png"
    }
  }
})
