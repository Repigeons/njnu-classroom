import encrypt from "./encrypt"

let app: WechatMiniprogram.App.Instance<IAppOption>
export function initialize(appInstance: WechatMiniprogram.App.Instance<IAppOption>) { app = appInstance }

function getCache(args: { path: string, request: boolean }): Promise<string | Record<string, any> | ArrayBuffer> {
    const url = `${app.globalData.server}${args.path}`
    const key = encrypt(url)
    if (args.request) {
        wx.request({
            url: url,
            success: res => wx.setStorage({
                key: key,
                data: res.data
            }),
            fail: console.error
        })
    }
    return new Promise((resolve, reject) => wx.getStorage({
        key: key,
        success: res => resolve(res.data),
        fail: () => wx.request({
            url: url,
            success: res => resolve(res.data),
            fail: reject
        })
    }))
}

export function getNotice(): Promise<INotice> {
    const url = `${app.globalData.server}/static/notice.json`
    return new Promise((resolve, reject) => {
        wx.request({
            url: url,
            success: res => resolve(res.data as INotice),
            fail: reject
        })
    })
}

export function getJxlPosition(request: boolean = false): Promise<Array<IPosition>> {
    return new Promise((resolve, reject) => {
        getCache({
            path: '/static/classroom/position.json',
            request
        })
            .then(data => resolve(data as Array<IPosition>))
            .catch(reject)
    })
}

export function getClassrooms(request: boolean = false): Promise<Record<string, Array<IJasInfo>>> {
    return new Promise((resolve, reject) => {
        getCache({
            path: '/static/classroom/list.json',
            request
        })
            .then(data => resolve(data as Record<string, Array<IJasInfo>>))
            .catch(reject)
    })
}

export function getZylxdm(request: boolean = false): Promise<Array<KeyValue>> {
    return new Promise((resolve, reject) => {
        getCache({
            path: '/static/classroom/zylxdm.json',
            request
        })
            .then(data => resolve(data as Array<KeyValue>))
            .catch(reject)
    })
}
export function getExploreGrids(request: boolean = false): Promise<Array<IGrid>> {
    return new Promise((resolve, reject) => {
        getCache({
            path: '/static/explore/grids.json',
            request
        })
            .then(data => resolve(data as Array<IGrid>))
            .catch(reject)
    })
}

export function getShuttle(day: number): Promise<IShuttle> {
    return new Promise((resolve, reject) => {
        getCache({
            path: `/explore/shuttle.json?day=${day}`,
            request: true
        })
            .then(data => {
                data = data as IJsonResponse
                resolve(data.data as IShuttle)
            })
            .catch(reject)
    })
}
