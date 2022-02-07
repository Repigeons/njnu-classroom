export enum Weekday {
  Sunday = "Sun.",
  Monday = "Mon.",
  Tuesday = "Tue.",
  Wednesday = "Wed.",
  Thursday = "Thu.",
  Friday = "Fri.",
  Saturday = "Sat.",
}

export const weekdays: Array<KeyValue> = [
  { key: 'Mon.', value: "周一" },
  { key: 'Tue.', value: "周二" },
  { key: 'Wed.', value: "周三" },
  { key: 'Thu.', value: "周四" },
  { key: 'Fri.', value: "周五" },
  { key: 'Sat.', value: "周六" },
  { key: 'Sun.', value: "周日" },
]
export function key2value(key: string) {
  return weekdays.find((item) => item.key == key)?.value
}
export function value2key(value: string) {
  return weekdays.find((item) => item.value == value)?.key
}
export const weekdays2: Array<KeyValue> = [
  { key: '#', value: "不限" },
  { key: 'Mon.', value: "周一" },
  { key: 'Tue.', value: "周二" },
  { key: 'Wed.', value: "周三" },
  { key: 'Thu.', value: "周四" },
  { key: 'Fri.', value: "周五" },
  { key: 'Sat.', value: "周六" },
  { key: 'Sun.', value: "周日" },
]