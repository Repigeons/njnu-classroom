const servers: Record<string, string> = {
  local: "http://njnu-classroom.local",
  develop: "https://t-classroom.njnu.xyz:8443",  // 开发版
  trial: "https://t-classroom.njnu.xyz:8443",  // 体验版
  release: "https://classroom.njnu.repigeons.cn",  // 正式版
}
const { envVersion } = wx.getAccountInfoSync().miniProgram as any
export const server =  servers[envVersion as string]

export function request(e: {
  path: string,
  method?: "OPTIONS" | "GET" | "HEAD" | "POST" | "PUT" | "DELETE" | "TRACE" | "CONNECT" | undefined,
  data?: string | Record<string, any> | ArrayBuffer | undefined
}): Promise<IJsonResponse> {
  const { path, method, data } = e
  return new Promise((resolve, reject) => {
    wx.request({
      url: `${server}${path}`,
      method, data,
      success(res) { resolve(res.data as IJsonResponse) },
      fail: reject
    })
  })
}

export function uploadFile(e: {
  path: string,
  filePath: string,
  formData?: any
}) {
  const { path, filePath, formData } = e
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: `${server}${path}`,
      name: 'file',
      filePath, formData,
      success(res) { resolve(JSON.parse(res.data)) },
      fail: reject
    })
  })
}
