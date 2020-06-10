using System;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Configuration.Json;

namespace dotnet
{
    public static class SettingService
    {
        public static IConfiguration AppSettings { get; private set; }
        public static IConfiguration DatabaseSettings { get; private set; }

        static SettingService()
        {
            AppSettings = new ConfigurationBuilder()
                .SetBasePath(AppDomain.CurrentDomain.BaseDirectory)
                .Add(new JsonConfigurationSource {Path = "appsettings.json", ReloadOnChange = true})
                .Build();
            DatabaseSettings = new ConfigurationBuilder()
                .SetBasePath(AppDomain.CurrentDomain.BaseDirectory)
                .Add(new JsonConfigurationSource {Path = "dbsettings.json", ReloadOnChange = true})
                .Build();
        }
    }
}