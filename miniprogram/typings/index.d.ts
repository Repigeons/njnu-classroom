/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    readonly server: string
  }
  flushStorage(): void
  preload(): void
}
