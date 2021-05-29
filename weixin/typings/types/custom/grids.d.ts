interface IGridNavigator {
  target?: string
  url?: string
  openType?: string
  delta?: number
  appId?: string
  path?: string
  extraData?: Object
  version?: string
  hoverStopPropagation?: boolean
  hoverStartTime?: number
  hoverStayTime?: number
  method?: string
}

interface IGridButton {
  openType?: "" | "contact" | "share" | "getPhoneNumber" | "getUserInfo" | "launchApp" | "openSetting" | "feedback"
  sessionFrom?: string
  sendMessageTitle?: string
  sendMessagePath?: string
  sendMessageImg?: string
  appParameter?: string
  showMessageCard?: boolean
}

interface IGrid extends IGridNavigator {
  text?: string
  imgUrl?: string
  button?: IGridButton
}
