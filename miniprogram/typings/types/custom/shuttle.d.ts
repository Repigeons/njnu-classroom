interface IShuttleRoute {
  readonly startTime: string
  readonly startStation: string
  readonly endStation: string
}

interface IShuttle {
  readonly stations: Array<IPosition>
  readonly direction1: Array<IShuttleRoute>
  readonly direction2: Array<IShuttleRoute>
}
