using System.Collections.Immutable;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace NjnuClassroom
{
    public class Startup
    {
        // This method gets called by the runtime. Use this method to add services to the container.
        // For more information on how to configure your application, visit https://go.microsoft.com/fwlink/?LinkID=398940
        public void ConfigureServices(IServiceCollection services)
        {
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            else
            {
                app.UseExceptionHandler("/Home/Error");
                app.UseHsts();
            }

            SettingService.SetEnv(env);
            app.Use(async (context, next) =>
            {
                context.Response.StatusCode = 400;
                context.Response.ContentType = "application/json";
                switch (context.Request.Path)
                {
                    case "/reset":
                        if (context.Request.Method != "POST")
                            break;
                        Index.Reset();
                        Overview.Reset();
                        context.Response.StatusCode = 202;
                        break;
                    case "/index.json":
                        if (context.Request.Method != "GET")
                            break;
                        await Index.ProcessRequest(context, context.Request.Query.ToImmutableDictionary());
                        break;
                    case "/searchmore.json":
                        if (context.Request.Method != "GET")
                            break;
                        await SearchMore.ProcessRequest(context, context.Request.Query.ToImmutableDictionary());
                        break;
                    case "/overview.json":
                        if (context.Request.Method != "GET")
                            break;
                        await Overview.ProcessRequest(context, context.Request.Query.ToImmutableDictionary());
                        break;
                    default:
                        await next();
                        break;
                }
            });
        }
    }
}