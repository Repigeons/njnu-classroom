/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    readonly server: string
    classrooms: Record<string, Array<IJasInfo>>
  }
  getNotice: () => Promise<INotice>
  getPositionJson: () => Promise<IJxlPosition>
  getClassrooms: () => Promise<Record<string, Array<IJasInfo>>>
  getZylxdm: () => Promise<Record<string, string>>
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
