/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    readonly server: string
  }
  getNotice(): Promise<INotice>
  getPosition(request?: boolean): Promise<IJxlPosition>
  getClassrooms(request?: boolean): Promise<Record<string, Array<IJasInfo>>>
  getZylxdm(request?: boolean): Promise<Record<string, string>>
  getShuttle(request?: boolean): Promise<IShuttle>
}

interface INotice {
  readonly date: string
  readonly timestamp: number
  readonly text: string
}

interface IJxlPosition extends Record<string, Array<number>> {}

interface IJasInfo {
  readonly JXLMC: string
  readonly JSMPH: string
  readonly JASDM: string
}

interface IShuttle {
  readonly stations: Array<string>
  readonly routes1: Array<Array<string>>
  readonly routes2: Array<Array<string>>
}
