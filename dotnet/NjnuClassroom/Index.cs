using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Primitives;
using ZTxLib.NETCore.DaoTemplate;
using ZTxLib.NETCore.DaoTemplate.MySQL;

namespace NjnuClassroom
{
    internal static class Index
    {
        /// <summary>
        /// 
        /// </summary>
        /// <param name="context"></param>
        /// <param name="parameters"></param>
        /// <returns></returns>
        public static async Task ProcessRequest(HttpContext context,
            ImmutableDictionary<string, StringValues> parameters)
        {
            if (SettingService.ConfigurationSettings["service"] == "off")
            {
                await context.Response.WriteAsync(Format(null, -1));
                return;
            }

            var jxl = parameters["jxl"];
            if (string.IsNullOrEmpty(jxl))
            {
                context.Response.StatusCode = 400;
                return;
            }

            if (!short.TryParse(parameters["day"], out var day))
            {
                context.Response.StatusCode = 400;
                return;
            }

            if (!short.TryParse(parameters["dqjc"], out var dqjc))
            {
                context.Response.StatusCode = 400;
                return;
            }

            if (UpdatedTime.Date != DateTime.Today)
                Reset(jxl, day);
            try
            {
                await context.Response.WriteAsync(Format(Buildings[jxl][day], dqjc));
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                throw;
            }
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="classrooms"></param>
        /// <param name="dqjc"></param>
        /// <returns></returns>
        private static string Format(IEnumerable<Classroom> classrooms, short dqjc)
        {
            var rank = 0;
            var service = SettingService.ConfigurationSettings["service"];
            var data = service == "on"
                ? $"[{string.Join(",", classrooms.Where(classroom => classroom.Jc_ks <= dqjc && classroom.Jc_js >= dqjc).Select(classroom => $"{{{string.Join(",", new Dictionary<string, string> {{"rank", (++rank).ToString()}, {"jxl", classroom.Jxl}, {"classroom", classroom.Jsmph}, {"jc_ks", classroom.Jc_ks.ToString()}, {"jc_js", classroom.Jc_js.ToString()}, {"zylxdm", classroom.Zylxdm}, {"capacity", classroom.Capacity.ToString()}, {"jyytms", classroom.Jyytms}, {"kcm", classroom.Kcm}}.Select(obj => $"\"{obj.Key}\":\"{obj.Value}\""))}}}"))}]"
                : "[]";
            return "{" +
                   "\"status\":0," +
                   "\"message\":\"ok\"," +
                   $"\"service\":\"{service}\"," +
                   $"\"data\":{data}" +
                   "}";
        }

        /// <summary>
        /// 更新时间
        /// </summary>
        private static DateTime UpdatedTime { get; set; } = DateTime.Today.AddDays(-1);

        /// <summary>
        /// 教学楼
        /// </summary>
        private static readonly Dictionary<string, List<Classroom>[]> Buildings =
            new Dictionary<string, List<Classroom>[]>();

        /// <summary>
        /// 初始化教学楼结构
        /// </summary>
        static Index()
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

            Reset();
        }

        /// <summary>
        /// 重置教学楼数据
        /// </summary>
        public static void Reset()
        {
            foreach (var building in Buildings.Keys)
                for (var day = 0; day < 7; day++)
                    Reset(building, day);
            UpdatedTime = DateTime.Today;
        }

        /// <summary>
        /// 重置教学楼数据
        /// </summary>
        private static void Reset(string name, int day)
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
            jxl[day].AddRange(new DataList<Classroom>(new Classroom.RowMapper(), dao));
            jxl[day].Sort((x, y) => -x.CompareTo(y));
        }
    }
}