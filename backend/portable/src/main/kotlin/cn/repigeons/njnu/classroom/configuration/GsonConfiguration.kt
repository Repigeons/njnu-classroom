package cn.repigeons.njnu.classroom.configuration

import com.google.gson.Gson
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
open class GsonConfiguration {
    @Bean
    open fun gson() = Gson()
}