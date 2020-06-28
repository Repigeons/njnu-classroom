/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    server: string,
    jxl: Array<IJxl>,
    lx: Array<ILx>,
  }
}

interface IJxl {
  name: string,
  pos: [number, number]
}

interface ILx {
  dm: string,
  name: string
}
