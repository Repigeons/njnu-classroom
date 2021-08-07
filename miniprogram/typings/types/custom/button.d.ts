interface IButton {
  readonly text: string,
  tap?: (e: any) => any,
  longpress?: (e: any) => any,
}
