interface IComponent {
  tap?: (e: any) => any,
  longpress?: (e: any) => any,
}

interface IButton extends IComponent {
  readonly text: string,
}

interface IClassDetailDialog {
  readonly detail: Array<{
    field: string
    value: string
  }>
  readonly title: any
}

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
