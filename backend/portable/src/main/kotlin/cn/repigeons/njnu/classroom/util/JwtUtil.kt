package cn.repigeons.njnu.classroom.util

import cn.repigeons.njnu.classroom.component.SpringContextHolder
import io.jsonwebtoken.Claims
import io.jsonwebtoken.Jwts
import io.jsonwebtoken.SignatureAlgorithm
import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Configuration
import java.util.*

@Configuration
private open class JwtConfig(
    @Value("\${jwt.secret:}")
    val secret: String,
    @Value("\${jwt.expire:0}")
    val expire: Int,
)

object JwtUtil {
    private val jwtConfig: JwtConfig = SpringContextHolder.getBean()
    const val TOKEN_HEAD = "Bearer"

    fun generate(claims: Claims): String {
        val issuedAt = System.currentTimeMillis()
        val expireAt = issuedAt + jwtConfig.expire * 1000
        val builder = Jwts.builder()
            .setClaims(claims)
            .setIssuedAt(Date(issuedAt))
            .setExpiration(Date(expireAt))
            .signWith(SignatureAlgorithm.HS256, jwtConfig.secret)
        return builder.compact()
    }

    fun parse(token: String): Claims? {
        try {
            return Jwts.parser()
                .setSigningKey(jwtConfig.secret)
                .parseClaimsJws(token)
                .body
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return null
    }
}