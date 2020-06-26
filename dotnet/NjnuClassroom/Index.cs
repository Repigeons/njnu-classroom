using System;
using System.Collections.Generic;
using System.Collections.Immutable;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Primitives;

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

            if (Today.Updated.Date != DateTime.Today)
                Today.Reset(jxl, day);
            try
            {
                await context.Response.WriteAsync(Format(Today.Buildings[jxl][day], dqjc));
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
            return
                $"[{string.Join(",", classrooms.Where(classroom => classroom.Jc_ks <= dqjc && classroom.Jc_js >= dqjc).Select(classroom => $"{{{string.Join(",", new Dictionary<string, string> {{"rank", (++rank).ToString()}, {"jxl", classroom.Jxl}, {"classroom", classroom.Jsmph}, {"jc_ks", classroom.Jc_ks.ToString()}, {"jc_js", classroom.Jc_js.ToString()}, {"zylxdm", classroom.Zylxdm}, {"capacity", classroom.Capacity.ToString()}, {"jyytms", classroom.Jyytms}, {"kcm", classroom.Kcm}}.Select(obj => $"\"{obj.Key}\":\"{obj.Value}\""))}}}"))}]";
        }
    }
}