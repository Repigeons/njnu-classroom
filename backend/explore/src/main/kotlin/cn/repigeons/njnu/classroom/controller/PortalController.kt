package cn.repigeons.njnu.classroom.controller

import cn.repigeons.njnu.classroom.common.JsonResponse
import cn.repigeons.njnu.classroom.common.Status
import cn.repigeons.njnu.classroom.model.Code2SessionResp
import cn.repigeons.njnu.classroom.util.JwtUtil
import io.jsonwebtoken.impl.DefaultClaims
import org.springframework.beans.factory.annotation.Value
import org.springframework.web.bind.annotation.GetMapping
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RequestParam
import org.springframework.web.bind.annotation.RestController
import org.springframework.web.client.RestTemplate
import org.springframework.web.client.getForObject
import org.springframework.web.util.UriComponentsBuilder

@RestController
@RequestMapping("sso")
class PortalController(
    private val restTemplate: RestTemplate,
    @Value("\${mp.appid}")
    private val appid: String,
    @Value("\${mp.secret}")
    private val secret: String,
) {
    @GetMapping("login")
    fun login(
        @RequestParam js_code: String
    ): JsonResponse {
        val url = UriComponentsBuilder
            .fromHttpUrl("https://api.weixin.qq.com/sns/jscode2session")
            .queryParam("appid", appid)
            .queryParam("secret", secret)
            .queryParam("js_code", js_code)
            .queryParam("grant_type", "authorization_code")
            .toUriString()
        val resp: Code2SessionResp = restTemplate.getForObject(url)
        if (resp.errcode != 0) {
            return JsonResponse(
                status = Status.FAILED,
                message = resp.errmsg
            )
        }
        val token = JwtUtil.generate(DefaultClaims().setSubject(resp.openid))
        return JsonResponse(
            Pair("token", token)
        )
    }
}