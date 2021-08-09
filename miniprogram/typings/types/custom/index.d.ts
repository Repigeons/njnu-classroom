interface KeyValue {
  readonly key: string
  readonly value: any
}

interface IPosition {
  rangeKey: string
  readonly name: string
  readonly position: {
    readonly 0: number
    readonly 1: number
  }
  readonly distance: number
  readonly number: number
}
