package cn.repigeons.njnu.classroom.component

import javax.servlet.*
import javax.servlet.annotation.WebFilter
import javax.servlet.http.HttpServletRequest
import javax.servlet.http.HttpServletResponse

@WebFilter(urlPatterns = ["/*"], filterName = "CharacterEncodingFilter")
class CharacterEncodingFilter : Filter {
    override fun init(filterConfig: FilterConfig) {}
    override fun destroy() {}
    override fun doFilter(servletRequest: ServletRequest, servletResponse: ServletResponse, filterChain: FilterChain) {
        val request = servletRequest as HttpServletRequest
        val response = servletResponse as HttpServletResponse
        request.characterEncoding = "UTF-8"
        response.characterEncoding = "UTF-8"
        filterChain.doFilter(request, response)
    }
}