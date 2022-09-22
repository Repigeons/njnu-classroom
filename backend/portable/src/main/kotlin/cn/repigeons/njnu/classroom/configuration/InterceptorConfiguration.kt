package cn.repigeons.njnu.classroom.configuration

import cn.repigeons.njnu.classroom.component.ServiceSwitchInterceptor
import org.springframework.context.annotation.Configuration
import org.springframework.web.servlet.config.annotation.InterceptorRegistry
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer

@Configuration
open class InterceptorConfiguration(
    private val serviceSwitchInterceptor: ServiceSwitchInterceptor
) : WebMvcConfigurer {
    override fun addInterceptors(registry: InterceptorRegistry) {
        registry.addInterceptor(serviceSwitchInterceptor)
            .excludePathPatterns("/switch")
    }
}