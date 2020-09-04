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
    public static class Overview
    {
        public static async Task ProcessRequest(HttpContext context,
            ImmutableDictionary<string, StringValues> parameters)
        {
            if (SettingService.ConfigurationSettings["service"] == "off")
            {
                await context.Response.WriteAsync(Format(null));
                return;
            }

            if (!parameters.ContainsKey("jasdm"))
            {
                context.Response.StatusCode = 400;
                return;
            }

            var jasdm = parameters["jasdm"];

            //TODO
            await context.Response.WriteAsync(Format(Buildings[jasdm]));
        }

        private static string Format(IEnumerable<Classroom> classrooms)
        {
            var id = 0;
            var service = SettingService.ConfigurationSettings["service"];
            var data = service == "on"
                ? $"[{string.Join(",", classrooms.Select(classroom => $"{{{string.Join(",", new Dictionary<string, object> {{"id", ++id}, {"jxl", classroom.Jxl}, {"classroom", classroom.Jsmph}, {"day", classroom.Day}, {"jc_ks", classroom.Jc_ks}, {"jc_js", classroom.Jc_js}, {"zylxdm", classroom.Zylxdm}, {"jyytms", classroom.Jyytms.Replace('\r', '\n').Replace("\n", "")}, {"kcm", classroom.Kcm.Replace('\r', '\n').Replace("\n", "")}}.Select(obj => $"\"{obj.Key}\":\"{obj.Value}\""))}}}"))}]"
                : "[]";
            return "{" +
                   "\"status\":0," +
                   "\"message\":\"ok\"," +
                   $"\"service\":\"{service}\"," +
                   $"\"data\":{data}" +
                   "}";
        }

        private static readonly Dictionary<string, List<Classroom>> Buildings =
            new Dictionary<string, List<Classroom>>();

        static Overview() => Reset();

        public static void Reset()
        {
            Buildings.Clear();
            var dao = SettingService.Dao;
            string[] days = {"sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"};
            for (var day = 0; day < 7; day++)
            {
                dao.Prepare($"SELECT * FROM `{days[day]}`");
                foreach (var classroom in new DataList<Classroom>(new ClassroomMapper(), dao))
                {
                    classroom.Day = day;
                    if (!Buildings.ContainsKey(classroom.Jasdm))
                        Buildings.Add(classroom.Jasdm, new List<Classroom>());
                    Buildings[classroom.Jasdm].Add(classroom);
                }
            }
        }
    }
}