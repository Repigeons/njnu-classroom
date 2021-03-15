export default function(str: string): number {
  let arr = str.split(':')
  if (arr.length != 2) {
    return NaN
  }
  let time_arr = arr.map(s => +s)
  if (time_arr[0] < 0 || time_arr[0] >= 24) {
    return NaN
  }
  if (time_arr[1] < 0 || time_arr[1] >= 60) {
    return NaN
  }
  return time_arr[0] * 60 + time_arr[1]
}
