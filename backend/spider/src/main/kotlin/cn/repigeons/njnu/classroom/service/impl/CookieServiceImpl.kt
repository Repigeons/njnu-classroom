package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.model.Cookies
import cn.repigeons.njnu.classroom.service.CookieService
import cn.repigeons.njnu.classroom.service.RedisService
import okhttp3.Cookie
import okhttp3.CookieJar
import okhttp3.HttpUrl
import okhttp3.OkHttpClient
import org.openqa.selenium.By
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service

@Service
class CookieServiceImpl(
    private val redisService: RedisService,
    @Value("\${account.username}")
    private val username: String,
    @Value("\${account.password}")
    private val password: String,
    @Value("\${account.gid}")
    private val gid: String,
) : CookieService {
    private val logger = LoggerFactory.getLogger(javaClass)
    private val driver: WebDriver

    init {
        val options = ChromeOptions()
        options.addArguments(
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--incognito",
        )
        driver = ChromeDriver(options)
    }

    override fun getCookies(): List<Cookie> {
        val cookies = redisService.get<List<Cookies>>("spider:cookies")
            ?.apply {
                redisService.set(
                    "spider:cookies",
                    this,
                    30 * 60
                )
            }
            ?: let {
                driver.get("http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/*default/index.do?amp_sec_version_=1&gid_=$gid")
                Thread.sleep(5000)
                logger.info("Login with user {}", username)
                driver.switchTo().defaultContent()
                driver.findElement(By.id("username")).sendKeys(username)
                driver.findElement(By.id("password")).sendKeys(password)
                driver.findElement(By.id("login_submit")).click()
                val cookies = driver.manage().cookies
                    .filter { it.name in listOf("MOD_AUTH_CAS", "_WEU") }
                    .map {
                        Cookies(
                            name = it.name,
                            value = it.value,
                            domain = it.domain,
                            path = it.path,
                        )
                    }
                redisService.set(
                    "spider:cookies",
                    cookies,
                    30 * 60
                )
                cookies
            }
        logger.info("Cookies = {}", cookies)
        return cookies.map {
            Cookie.Builder()
                .name(it.name)
                .value(it.value)
                .domain(it.domain)
                .path(it.path)
                .build()
        }
    }

    override fun getHttpClient(cookies: List<Cookie>): OkHttpClient {
        return OkHttpClient.Builder()
            .cookieJar(object : CookieJar {
                override fun loadForRequest(url: HttpUrl) = cookies
                override fun saveFromResponse(url: HttpUrl, cookies: List<Cookie>) {}
            })
            .build()
    }
}