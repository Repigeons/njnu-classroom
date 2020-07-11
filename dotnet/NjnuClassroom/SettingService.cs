using System;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.Json;

namespace NjnuClassroom
{
    public static class SettingService
    {
        public static IConfiguration AppSettings { get; }
        public static IConfiguration ConfigurationSettings { get; }
        public static IConfiguration DatabaseSettings { get; }

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
                .Build()
                .GetSection(ConfigurationSettings["environment"]);
        }
    }
}
