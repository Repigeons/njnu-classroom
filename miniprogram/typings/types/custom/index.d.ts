interface KeyValue {
  readonly key: string
  readonly value: any
}

interface IPosition {
  readonly name: string
  readonly position: {
    readonly 0: number
    readonly 1: number
  }
  readonly distance: number
}
