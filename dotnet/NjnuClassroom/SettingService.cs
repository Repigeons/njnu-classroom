using System;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.Json;
using Microsoft.Extensions.Hosting;
using ZTxLib.NETCore.DaoTemplate.MySQL;

namespace NjnuClassroom
{
    public static class SettingService
    {
        public static IConfiguration AppSettings { get; }
        public static IConfiguration ConfigurationSettings { get; }
        public static IConfiguration DatabaseSettings { get; }

        /// <summary>
        /// runtime environment
        /// </summary>
        private static IWebHostEnvironment _env;

        /// <summary>
        /// Data Access Object
        /// </summary>
        public static Dao Dao { get; private set; }

        static SettingService()
        {
            AppSettings = new ConfigurationBuilder()
                .SetBasePath(AppDomain.CurrentDomain.BaseDirectory)
                .Add(new JsonConfigurationSource {Path = "appsettings.json", ReloadOnChange = true})
                .Build();

            ConfigurationSettings = new ConfigurationBuilder()
                .SetBasePath(AppDomain.CurrentDomain.BaseDirectory)
                .Add(new JsonConfigurationSource {Path = "conf/config.json", ReloadOnChange = true})
                .Build();

            DatabaseSettings = new ConfigurationBuilder()
                .SetBasePath(AppDomain.CurrentDomain.BaseDirectory)
                .Add(new JsonConfigurationSource {Path = "conf/database.json", ReloadOnChange = true})
                .Build();

            SetEnv(_env);
        }

        public static void SetEnv(IWebHostEnvironment env)
        {
            if (DatabaseSettings == null || env == null || Dao != null)
                return;
            _env = env;
            var database = DatabaseSettings.GetSection(
                env.IsDevelopment() ? "dev" : "pro"
            );
            Dao = new Dao(new DataSource(
                database["host"],
                short.Parse(database["port"]),
                database["user"],
                database["password"],
                database["database"]
            ));
        }
    }
}