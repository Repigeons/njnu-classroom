import {Md5} from "./md5"

export default (str: string) => (Md5.hashStr(str) as string).substr(8, 8)
