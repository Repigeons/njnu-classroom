using System.Collections.Immutable;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace dotnet
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
                app.UseDeveloperExceptionPage();
            app.Use(async (context, next) =>
            {
                context.Response.ContentType = "application/json";
                var parameters = (context.Request.Method == "GET")
                    ? context.Request.Query.ToImmutableDictionary()
                    : context.Request.Form.ToImmutableDictionary();

                switch (context.Request.Path)
                {
                    case "/":
                        Today.Reset();
                        context.Response.StatusCode = 202;
                        break;
                    case "/index.json":
                        await Index.ProcessRequest(context, parameters);
                        break;
                    case "/searchmore.json":
                        await SearchMore.ProcessRequest(context, parameters);
                        break;
                    default:
                        await next();
                        break;
                }
            });
        }
    }
}