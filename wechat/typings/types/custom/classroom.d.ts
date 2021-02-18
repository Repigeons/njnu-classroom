interface IJxlPosition extends Record<string, Array<number>> {}

interface IJasInfo {
  readonly JXLMC: string
  readonly JSMPH: string
  readonly JASDM: string
}

interface IClassroomInfo extends Record<string, any> {
  /**
   * 标题
   */
  title: string,
  /**
   * 课程占用
   */
  KCZYFLAG?: boolean,
  /**
   * 本科生考试
   */
  BKSKSZYFLAG?: boolean,
  /**
   * 普通教室借用占用
   */
  PTJYZYFLAG?: boolean,
  /**
   * 屏蔽占用
   */
  PBZYFLAG?: boolean,
  /**
   * 课程占用
   */
  FBKSPKZYFLAG?:boolean,
  /**
     * 开课单位
   */
  KKDW?: string,
  /**
   * 上课教师
   */
  SKJS?: string,
  /**
   * 课程名称
   */
  KCMC?: string,
  /**
   * 选课人数
   */
  XKRS?: number,
  /**
   * 行政班
   */
  XZB?: string,
  /**
   * 借用单位
   */
  JYDW?: string,
  /**
   * 借用人姓名
   */
  JYRXM?: string,
  /**
   * 负责老师
   */
  FZLS?: string,
  /**
   * 联系人电话
   */
  LXDH?: string,
  /**
   * 借用说明
   */
  JYYTMS?: string,
  /**
   * 上课人数
   */
  SKRS?: string,
  /**
   * 
   */
  PKLY?: string,
}

interface IClassroomRow extends Record<string, any> {
  id: number,
  JXLMC: string,
  jsmph: string,
  day: number,
  jc_ks: number,
  jc_js: number,
  zylxdm: string,
  jyytms: string,
  kcm: string,
}