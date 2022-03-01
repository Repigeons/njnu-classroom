import { request } from "./http"

async function getCache(args: { path: string, request: boolean }): Promise<string | Record<string, any> | ArrayBuffer> {
    if (args.request) {
        const res = await request({
            path: args.path
        })
        wx.setStorage({
            key: args.path,
            data: res.data
        })
    }
    try {
        return wx.getStorageSync(args.path)
    } catch {
        const res = await request({
            path: args.path
        })
        wx.setStorage({
            key: args.path,
            data: res.data
        })
        return res.data
    }
}

export async function getClassrooms(request: boolean = false): Promise<Record<string, Array<IJasInfo>>> {
    return await getCache({
        path: '/api/classrooms.json',
        request
    }) as Record<string, Array<IJasInfo>>
}

export async function getJxlPosition(request: boolean = false): Promise<Array<IPosition>> {
    return await getCache({
        path: '/api/position.json',
        request
    }) as Array<IPosition>
}

export async function getZylxdm(request: boolean = false): Promise<Array<KeyValue>> {
    return await getCache({
        path: '/api/zylxdm.json',
        request
    }) as Array<KeyValue>
}

export async function getExploreGrids(request: boolean = false): Promise<Array<IGrid>> {
    return await getCache({
        path: '/explore/grids.json',
        request
    }) as Array<IGrid>
}

export async function getShuttle(day: string, request: boolean = false): Promise<IShuttle> {
    return await getCache({
        path: `/explore/shuttle.json?day=${day}`,
        request
    }) as IShuttle
}
