interface IShuttleRoute extends Array<string> { }

interface IShuttle {
  readonly stations: Array<IPosition>
  readonly direction1: Array<IShuttleRoute>
  readonly direction2: Array<IShuttleRoute>
}
