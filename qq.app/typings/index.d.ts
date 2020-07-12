/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    readonly server: string,
    readonly jxl: Array<IJxl>,
    readonly lx: Array<ILx>,
  }
}

interface IJxl {
  readonly name: string,
  readonly pos: [number, number]
}

interface ILx {
  readonly dm: string,
  readonly name: string
}
