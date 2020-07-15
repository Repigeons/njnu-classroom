using System;
using System.Collections.Generic;
using ZTxLib.NETCore.DaoTemplate;
using ZTxLib.NETCore.DaoTemplate.MySQL;

namespace NjnuClassroom
{
    public static class Today
    {
        /// <summary>
        /// 更新时间
        /// </summary>
        public static DateTime Updated { get; private set; } = DateTime.Today.AddDays(-1);

        /// <summary>
        /// 教学楼
        /// </summary>
        public static readonly Dictionary<string, List<Classroom>[]> Buildings =
            new Dictionary<string, List<Classroom>[]>();

        /// <summary>
        /// 初始化教学楼结构
        /// </summary>
        static Today()
        {
            foreach (var building in new[]
            {
                "信息楼", "电教楼", "学明楼", "学正楼", "学海楼", "广乐楼", "学行楼", "学思楼"
            })
            {
                Buildings.Add(building, new[]
                {
                    new List<Classroom>(), new List<Classroom>(), new List<Classroom>(), new List<Classroom>(),
                    new List<Classroom>(), new List<Classroom>(), new List<Classroom>()
                });
            }
        }

        /// <summary>
        /// 重置教学楼数据
        /// </summary>
        public static void Reset()
        {
            foreach (var building in Buildings.Keys)
                for (var day = 0; day < 7; day++)
                    Reset(building, day);
            Updated = DateTime.Today;
        }

        /// <summary>
        /// 重置教学楼数据
        /// </summary>
        public static void Reset(string name, int day)
        {
            var dao = SettingService.Dao;
            var jxl = Buildings[name];
            jxl[day].Clear();
            string[] days = {"sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"};
            dao.Prepare(
                "SELECT * FROM `${day}` WHERE `jxl`=#{jxl} AND `zylxdm` in ('00','10') ORDER BY `zylxdm`",
                concat: new[]
                {
                    new KvPair("day", days[day]),
                },
                parameter: new[]
                {
                    new KvPair("jxl", name),
                }
            );
            jxl[day].AddRange(new DataList<Classroom>(new ClassroomMapper(), dao));
            jxl[day].Sort((x, y) => -x.CompareTo(y));
        }
    }
}