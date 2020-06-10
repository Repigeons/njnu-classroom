using MySql.Data.MySqlClient;
using ZTxLib.NETCore.DaoTemplate.MySQL;

namespace dotnet
{
    public class ClassroomMapper : IRowMapper<Classroom>
    {
        public Classroom MapRow(MySqlDataReader reader, int index) => new Classroom
        {
            Jasdm = (string) reader["jasdm"],
            Jxl = (string) reader["jxl"],
            Jsmph = (string) reader["jsmph"],
            Zylxdm = (string) reader["zylxdm"],
            Jc_ks = (int) reader["jc_ks"],
            Jc_js = (int) reader["jc_js"],
            Jyytms = (string) reader["jyytms"],
            Kcm = (string) reader["kcm"]
        };
    }
}