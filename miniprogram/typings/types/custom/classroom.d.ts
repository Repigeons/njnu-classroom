interface IJasInfo extends Record<string, any> {
  readonly JXLMC: string
  readonly JSMPH: string
  readonly JASDM: string
}

interface IClassroomInfo extends Record<string, any> {
  /**
   * 标题
   */
  readonly title: string,
  /**
   * 课程占用
   */
  readonly KCZYFLAG?: boolean,
  /**
   * 本科生考试
   */
  readonly BKSKSZYFLAG?: boolean,
  /**
   * 普通教室借用占用
   */
  readonly PTJYZYFLAG?: boolean,
  /**
   * 屏蔽占用
   */
  readonly PBZYFLAG?: boolean,
  /**
   * 课程占用
   */
  readonly FBKSPKZYFLAG?: boolean,
  /**
     * 开课单位
   */
  readonly KKDW?: string,
  /**
   * 上课教师
   */
  readonly SKJS?: string,
  /**
   * 课程名称
   */
  readonly KCMC?: string,
  /**
   * 选课人数
   */
  readonly XKRS?: number,
  /**
   * 行政班
   */
  readonly XZB?: string,
  /**
   * 借用单位
   */
  readonly JYDW?: string,
  /**
   * 借用人姓名
   */
  readonly JYRXM?: string,
  /**
   * 负责老师
   */
  readonly FZLS?: string,
  /**
   * 联系人电话
   */
  readonly LXDH?: string,
  /**
   * 借用说明
   */
  readonly JYYTMS?: string,
  /**
   * 上课人数
   */
  readonly SKRS?: number,
  /**
   *
   */
  readonly PKLY?: string,
}

interface IClassroomRow extends Record<string, any> {
  id: number,
  JXLMC: string,
  jsmph: string,
  day: string,
  jc_ks: number,
  jc_js: number,
  zylxdm: string,
  jyytms: string,
  kcm: string,
}
