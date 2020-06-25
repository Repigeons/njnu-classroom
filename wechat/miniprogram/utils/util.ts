export const formatTime = (date: Date) => {
  const year = date.getFullYear()
  const month = date.getMonth() + 1
  const day = date.getDate()
  const hour = date.getHours()
  const minute = date.getMinutes()
  const second = date.getSeconds()

  return (
    [year, month, day].map(formatNumber).join('/') +
    ' ' +
    [hour, minute, second].map(formatNumber).join(':')
  )
}

const formatNumber = (n: number) => {
  const s = n.toString()
  return s[1] ? s : '0' + s
}

const getSpan = (hour: number, minute: number): number => {
  return hour * 60 + minute
}

export const jc = (datetime: Date): number => {
  // 当前时间
  const span = getSpan(datetime.getHours(), datetime.getMinutes())
  const jc_list = [
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
export const distance = ({ longitude1, latitude1, longitude2, latitude2 }: AnyObject): number => {
  let Rad = (d: number) => d * Math.PI / 180.0
  let radLat1 = Rad(latitude1)
  let radLat2 = Rad(latitude2)
  let a = radLat1 - radLat2
  let b = Rad(longitude1) - Rad(longitude2)
  let s = 2 * Math.asin(Math.sqrt(Math.pow(Math.sin(a/2),2) + Math.cos(radLat1)*Math.cos(radLat2)*Math.pow(Math.sin(b/2),2)))
  s = s *6378.137  // EARTH_RADIUS
  s = Math.round(s * 1000000) / 1000  //输出为米
  return s
}
