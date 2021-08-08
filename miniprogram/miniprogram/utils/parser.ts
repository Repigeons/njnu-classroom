export const parseKcm = (zylxdm: string, KCM: string): IClassroomInfo | null => {
  let kcxx: Array<string>
  const pklysz: Record<string, string> = { '01': '研', '02': '成', '03': '本', '04': '借', '05': '本考', '11': '研考', '12': '成教' }
  switch (zylxdm) {
    case '01':
    case '03':
      // 课程占用
      kcxx = KCM.replace(/%%/g, ',').split("#")
      return {
        KCZYFLAG: true,
        // 开课单位
        KKDW: kcxx[0] ? kcxx[0] : '',
        // 上课教师
        SKJS: kcxx[1] ? kcxx[1] : '',
        // 课程名称
        KCMC: kcxx[2] ? kcxx[2] : '',
        // 选课人数
        XKRS: kcxx[3] ? +kcxx[3] : 0,
        // 行政班
        XZB: kcxx[4] ? kcxx[4] : '',
        //
        title: kcxx[2] ? kcxx[2] : '未知',
      }
      break
    case '02':
      // 本科生考试
      return {
        BKSKSZYFLAG: true,
        //
        PKLY: pklysz['05'],
        //
        title: KCM,
      }
      break
    case '04':
      // 普通教室借用占用
      kcxx = KCM.split("#")
      return {
        PTJYZYFLAG: true,
        // 借用单位
        JYDW: kcxx[0] ? kcxx[0] : '',
        // 借用人姓名
        JYRXM: kcxx[1] ? kcxx[1] : '',
        // 负责老师
        FZLS: kcxx[2] ? kcxx[2] : '',
        // 联系人电话
        LXDH: kcxx[3] ? kcxx[3] : '',
        // 借用说明
        JYYTMS: kcxx[4] ? kcxx[4] : '',
        //
        PKLY: pklysz['04'],
        //
        title: kcxx[4] ? kcxx[4] : '未知',
      }
      break
    case '05':
      // 屏蔽占用
      return {
        title: '教室资源屏蔽',
        PBZYFLAG: true,
      }
      break
    case '10':
    case '11':
      // 课程占用
      kcxx = KCM.split("#")
      return {
        FBKSPKZYFLAG: true,
        // 课程名称
        KCMC: kcxx[0] ? kcxx[0] : '',
        // 上课教师
        SKJS: kcxx[1] ? kcxx[1] : '',
        // 上课人数
        SKRS: kcxx[2] ? +kcxx[2] : 0,
        // 借用单位
        JYDW: kcxx[3] ? kcxx[3] : '',
        // 借用人姓名
        JYRXM: kcxx[4] ? kcxx[4] : '',
        // 负责老师
        FZLS: kcxx[5] ? kcxx[5] : '',
        // 联系电话
        LXDH: kcxx[6] ? kcxx[6] : '',
        //
        PKLY: pklysz[kcxx[7]],
        //
        title: kcxx[0] ? kcxx[0] : '未知',
      }
      break
    default:
      return null
  }
}

export const item2dialog = (item: Record<string, any>, rq: string) => {
  const title: string = item.title
  const detail: Array<{
    field: string;
    value: string;
  }> = [
      { field: '教室门牌', value: `${item.JXLMC}${item.jsmph}` },
      { field: '使用时间', value: `${rq}${item.jc_ks}-${item.jc_js}节` },
    ]
  if (item.KCMC) detail.push({ field: '课程名称', value: item.KCMC })
  if (item.SKJS) detail.push({ field: '上课教师', value: item.SKJS })
  if (item.KKDW) detail.push({ field: '开课单位', value: item.KKDW })
  if (item.XKRS) detail.push({ field: '选课人数', value: item.XKRS })
  if (item.SKRS) detail.push({ field: '上课人数', value: item.SKRS })
  // if (item.XZB) detail.push({ field: '行政班级', value: item.XZB })
  if (item.JYDW) detail.push({ field: '借用单位', value: item.JYDW })
  if (item.JYRXM) detail.push({ field: '借用人姓名', value: item.JYRXM })
  if (item.FZLS) detail.push({ field: '负责老师', value: item.FZLS })
  // if (item.LXDH) detail.push({ field: '联系电话', value: item.LXDH })
  if (item.JYYTMS) detail.push({ field: '借用说明', value: item.JYYTMS })
  else if (item.jyytms) detail.push({ field: '借用说明', value: item.jyytms })
  return { title, detail }
}
