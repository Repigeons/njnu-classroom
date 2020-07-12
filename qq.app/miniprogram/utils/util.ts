const getSpan = (hour: number, minute: number): number => {
  return hour * 60 + minute
}

export const getJc = (datetime: Date): number => {
  // 当前时间
  const span: number = getSpan(datetime.getHours(), datetime.getMinutes())
  const jc_list: Array<number> = [
    getSpan(8, 40),
    getSpan(9, 25),
    getSpan(10, 20),
    getSpan(11, 15),
    getSpan(12, 0),
    getSpan(14, 10),
    getSpan(14, 55),
    getSpan(15, 50),
    getSpan(16, 35),
    getSpan(19, 10),
    getSpan(20, 0),
    getSpan(20, 50)
  ]
  for (let i = 0; i < 12; i++)
    if (span < jc_list[i])
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
  let s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a/2),2) + Math.cos(radLat1)*Math.cos(radLat2)*Math.pow(Math.sin(b/2),2)))
  s = s *6378.137  // EARTH_RADIUS
  return Math.round(s * 1000000) / 1000  //输出为米
}
