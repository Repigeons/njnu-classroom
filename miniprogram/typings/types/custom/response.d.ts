interface IJsonResponse {
  readonly status: number
  readonly message?: string
  readonly data?: any
}

interface IPageResult {
  readonly page: number
  readonly size: number
  readonly pageCount: number
  readonly totalCount: number
  readonly list: Array<any>
}
