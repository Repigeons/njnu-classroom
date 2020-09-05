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
    internal static class SearchMore
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
                await context.Response.WriteAsync(
                    "{" +
                    "\"status\":1," +
                    "\"message\":\"service off\"," +
                    $"\"service\":\"off\"," +
                    $"\"data\":[]" +
                    "}");
                return;
            }

            var dao = SettingService.Dao;
            string[] days = {"sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"};

            if (new[] {"day", "jc_ks", "jc_js", "jxl", "zylxdm", "kcm"}.Any(key => !parameters.ContainsKey(key)))
            {
                context.Response.StatusCode = 400;
                return;
            }

            var day = parameters["day"];
            var jc_ks = parameters["jc_ks"];
            var jc_js = parameters["jc_js"];
            var jxl = parameters["jxl"];
            var zylxdm = parameters["zylxdm"];
            var kcm = parameters["kcm"];
            if (kcm == "#") kcm = "_";
            if (day != "#") days = new[] {days[int.Parse(day)]};
            var jc = $"(`jc_ks`>={jc_ks} AND `jc_js`<={jc_js})";
            jxl = jxl == "#" ? "(`jxl` IS NOT NULL)" : $"(`jxl`='{jxl}')";
            zylxdm = zylxdm == "#" ? "(`zylxdm` IS NOT NULL)" : $"(`zylxdm`='{zylxdm}')";

            var classrooms = new List<Classroom>();
            for (var d = 0; d < days.Length; d++)
            {
                dao.Prepare(
                    "SELECT * FROM `${day}` WHERE ${jc} AND ${jxl} AND ${zylxdm} AND (`jyytms` LIKE #{kcm} OR `kcm` LIKE #{kcm})",
                    concat: new[]
                    {
                        new KvPair("day", days[d]),
                        new KvPair("jc", jc),
                        new KvPair("jxl", jxl),
                        new KvPair("zylxdm", zylxdm),
                    },
                    parameter: new[]
                    {
                        new KvPair("kcm", $"%{kcm}%"),
                    }
                );
                foreach (var classroom in new DataList<Classroom>(new Classroom.RowMapper(), dao))
                {
                    classroom.Day = (day == "#") ? d : int.Parse(day);
                    classrooms.Add(classroom);
                }
            }

            await context.Response.WriteAsync(Format(classrooms));
        }

        /// <summary>
        /// 
        /// </summary>
        /// <param name="classrooms"></param>
        /// <returns></returns>
        private static string Format(IEnumerable<Classroom> classrooms)
        {
            var id = 0;
            var data =
                $"[{string.Join(",", classrooms.Select(classroom => $"{{{string.Join(",", new Dictionary<string, object> {{"id", ++id}, {"jxl", classroom.Jxl}, {"classroom", classroom.Jsmph}, {"day", classroom.Day}, {"jc_ks", classroom.Jc_ks}, {"jc_js", classroom.Jc_js}, {"zylxdm", classroom.Zylxdm}, {"jyytms", classroom.Jyytms.Replace('\r', '\n').Replace("\n", "")}, {"kcm", classroom.Kcm.Replace('\r', '\n').Replace("\n", "")}}.Select(obj => $"\"{obj.Key}\":\"{obj.Value}\""))}}}"))}]";
            return "{" +
                   "\"status\":0," +
                   "\"message\":\"ok\"," +
                   $"\"service\":\"on\"," +
                   $"\"data\":{data}" +
                   "}";
        }
    }
}