/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    readonly server: string
  }
  flushStorage(): void
  preload(): void
  _getCache(args: {url: string, request: boolean}): Promise<string|Record<string,any>|ArrayBuffer>
  getNotice(): Promise<INotice>
  getJxlPosition(request?: boolean): Promise<Array<IPosition>>
  getClassrooms(request?: boolean): Promise<Record<string, Array<IJasInfo>>>
  getZylxdm(request?: boolean): Promise<Record<string, string>>
  getExploreGrids(request?: boolean): Promise<Array<IGrid>>
  getShuttle(request?: boolean): Promise<IShuttle>
}
