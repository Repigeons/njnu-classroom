/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    readonly server: string
  }
  clearStorage(): void
  preload(): void
  getNotice(): Promise<INotice>
  getPosition(request?: boolean): Promise<IJxlPosition>
  getClassrooms(request?: boolean): Promise<Record<string, Array<IJasInfo>>>
  getZylxdm(request?: boolean): Promise<Record<string, string>>
  getShuttle(request?: boolean): Promise<IShuttle>
  getExploreGrids(request?: boolean): Promise<Array<IGrid>>
}
