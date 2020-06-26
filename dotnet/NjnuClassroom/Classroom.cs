namespace NjnuClassroom
{
    public class Classroom
    {
        /// <summary>
        /// 星期几
        /// </summary>
        public int Day { get; set; }

        /// <summary>
        /// ？？？
        /// </summary>
        public string Jasdm { get; set; }

        /// <summary>
        /// 教学楼
        /// </summary>
        public string Jxl { get; set; }

        /// <summary>
        /// 教室门牌号
        /// </summary>
        public string Jsmph { get; set; }

        /// <summary>
        /// 教室容纳人数
        /// </summary>
        public int Capacity { get; set; }

        /// <summary>
        /// ？？？
        /// </summary>
        public string Zylxdm { get; set; }

        /// <summary>
        /// 开始节次
        /// </summary>
        public int Jc_ks { get; set; }

        /// <summary>
        /// 结束节次
        /// </summary>
        public int Jc_js { get; set; }

        /// <summary>
        /// 借用用途说明
        /// </summary>
        public string Jyytms { get; set; }

        /// <summary>
        /// 课程名
        /// </summary>
        public string Kcm { get; set; }

        public void set_jcJs(int jcJs) => Jc_js = jcJs;
        public void set_zylxdm(string zylxdm) => Zylxdm = (zylxdm == "10") ? "10" : Zylxdm;

        public int CompareTo(Classroom classroom)
        {
            if (Zylxdm != classroom.Zylxdm)
                // "00" 优先于 "10"
                return string.CompareOrdinal(classroom.Zylxdm, Zylxdm);
            if (Jc_js != classroom.Jc_js)
                // 结束节次 大值优先
                return Jc_js - classroom.Jc_js;
            // 门牌号 小值优先
            return string.CompareOrdinal(classroom.Jsmph, Jsmph);
        }
    }
}