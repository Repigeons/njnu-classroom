interface IGridNavigator {
  readonly target?: string
  readonly url?: string
  readonly openType?: string
  readonly delta?: number
  readonly appId?: string
  readonly path?: string
  readonly extraData?: Object
  readonly version?: string
  readonly hoverStopPropagation?: boolean
  readonly hoverStartTime?: number
  readonly hoverStayTime?: number
  readonly method?: string
}

interface IGridButton {
  readonly openType?: "" | "contact" | "share" | "getPhoneNumber" | "getUserInfo" | "launchApp" | "openSetting" | "feedback"
  readonly sessionFrom?: string
  readonly sendMessageTitle?: string
  readonly sendMessagePath?: string
  readonly sendMessageImg?: string
  readonly appParameter?: string
  readonly showMessageCard?: boolean
}

interface IGrid extends IGridNavigator {
  readonly text?: string
  readonly imgUrl?: string
  button?: IGridButton
}
