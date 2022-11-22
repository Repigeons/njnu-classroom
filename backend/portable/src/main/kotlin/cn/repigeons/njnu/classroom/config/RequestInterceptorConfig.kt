package cn.repigeons.njnu.classroom.config

import cn.repigeons.njnu.classroom.component.ServiceSwitchInterceptor
import org.springframework.context.annotation.Configuration
import org.springframework.web.servlet.config.annotation.InterceptorRegistry
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer

@Configuration
open class RequestInterceptorConfig(
    private val serviceSwitchInterceptor: ServiceSwitchInterceptor
) : WebMvcConfigurer {
    override fun addInterceptors(registry: InterceptorRegistry) {
        registry.addInterceptor(serviceSwitchInterceptor)
            .excludePathPatterns("/switch")
    }
}