import * as md5 from "md5"

export const md5_32 = (s: string) => md5(s)
export const md5_16 = (s: string) => md5(s).substr(8, 16)

export default md5_16
