/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    readonly server: string,
    readonly jxl: Array<IJxl>,
    readonly lx: Array<ILx>,
    classrooms: Record<string, Array<object>>
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
