export const formatTime = (datetime: Date): string => {
  const hours = datetime.getHours()
  const minutes = datetime.getMinutes()
  return `${hours > 9 ? '' : '0'}${hours}:${minutes > 9 ? '' : '0'}${minutes}`
}

export const getTimeSpan = (hour: number, minute: number): number => {
  return hour * 60 + minute
}

export const getJc = (datetime: Date): number => {
  // 当前时间
  const span: number = getTimeSpan(datetime.getHours(), datetime.getMinutes())
  const jcList: Array<number> = [
    getTimeSpan(8, 40),
    getTimeSpan(9, 25),
    getTimeSpan(10, 20),
    getTimeSpan(11, 15),
    getTimeSpan(12, 0),
    getTimeSpan(14, 10),
    getTimeSpan(14, 55),
    getTimeSpan(15, 50),
    getTimeSpan(16, 35),
    getTimeSpan(19, 10),
    getTimeSpan(20, 0),
    getTimeSpan(20, 50)
  ]
  for (let i = 0; i < 12; i++)
    if (span < jcList[i])
      return i
  return 11
}

//计算距离，参数分别为第一点的纬度，经度；第二点的纬度，经度
export const getDistance = (e: {
  longitude1: number
  latitude1: number
  longitude2: number
  latitude2: number
}): number => {
  const { longitude1, latitude1, longitude2, latitude2 } = e
  const Rad = (d: number) => d * Math.PI / 180.0
  const radLat1 = Rad(latitude1)
  const radLat2 = Rad(latitude2)
  const a = radLat1 - radLat2
  const b = Rad(longitude1) - Rad(longitude2)
  let s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a / 2), 2) + Math.cos(radLat1) * Math.cos(radLat2) * Math.pow(Math.sin(b / 2), 2)))
  s = s * 6378.137  // EARTH_RADIUS
  return Math.round(s * 1000000) / 1000  //输出为米
}
