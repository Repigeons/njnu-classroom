// components/grids/grids.js
const navigatorDefault: IGridNavigator = {
  target: 'self',
  url: '',
  openType: 'navigate',
  delta: 1,
  appId: '',
  path: '',
  extraData: '',
  version: 'release',
  hoverStopPropagation: false,
  hoverStartTime: 50,
  hoverStayTime: 600,
  tap: ''
},
buttonDefault: IGridButton = {
  openType: '',
  sessionFrom: '',
  sendMessageTitle: '',
  sendMessagePath: '',
  sendMessageImg: '',
  appParameter: '',
  showMessageCard: false,
}

Component({
  /**
   * 组件的属性列表
   */
  properties: {
    grids: { type: Array }
  },

  /**
   * 组件的初始数据
   */
  data: {
    innerGrids: Array<IGrid>()
  },

  /**
   * 组件的方法列表
   */
  methods: {
    onGridTap(e) {
      this.triggerEvent('tapgrids', {'method': e.currentTarget.dataset.method})
    }
  },
  observers: {
    grids(grids: Array<IGrid>) {
      this.setData({
        innerGrids: grids.map((grid: IGrid) => {
          grid.button = grid.button ? (<any>Object).assign({}, buttonDefault, grid.button) : grid.button
          return (<any>Object).assign({}, navigatorDefault, grid)
        })
      })
    }
  }
})
