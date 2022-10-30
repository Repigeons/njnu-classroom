package cn.repigeons.njnu.classroom.configuration

import org.springframework.http.MediaType
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter

internal class RestTemplateMessageConverter : MappingJackson2HttpMessageConverter() {
    init {
        val mediaTypes: MutableList<MediaType> = ArrayList()
        mediaTypes.add(MediaType.APPLICATION_JSON)
        mediaTypes.add(MediaType.TEXT_PLAIN)
        supportedMediaTypes = mediaTypes
    }
}