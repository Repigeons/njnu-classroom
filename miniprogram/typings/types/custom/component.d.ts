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