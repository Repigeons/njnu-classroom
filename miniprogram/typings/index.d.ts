/// <reference path="./types/index.d.ts" />

interface IAppOption {
  globalData: {
    server: string
  }
  flushStorage(): void
  preload(): void
}
