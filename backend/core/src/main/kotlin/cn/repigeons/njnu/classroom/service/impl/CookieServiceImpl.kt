package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.service.CookieService
import cn.repigeons.njnu.classroom.service.RedisService
import cn.repigeons.njnu.classroom.util.GsonUtil
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
    @Value("\${browser-debugger.address:127.0.0.1}")
    private val browserAddr: String,
    @Value("\${browser-debugger.port:9222}")
    private val browserPort: Int,
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
        var chromeDriver: ChromeDriver
        val options = ChromeOptions()
        options.setExperimentalOption("debuggerAddress", "$browserAddr:$browserPort")
        while (true) {
            try {
                chromeDriver = ChromeDriver(options)
                break
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        driver = chromeDriver
    }

    override fun getCookies(): List<Cookie> {
        val cookies = redisService["spider:cookies"]?.let {
            GsonUtil.fromJson<List<Map<String, String>>>(it)
        } ?: let {
            driver.get("http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/*default/index.do?amp_sec_version_=1&gid_=$gid")
            Thread.sleep(5000)
            driver.switchTo().defaultContent()
            driver.findElement(By.id("username")).sendKeys(username)
            driver.findElement(By.id("password")).sendKeys(password)
            driver.findElement(By.id("login_submit")).click()
            val cookies = driver.manage().cookies
                .filter { it.name in listOf("MOD_AUTH_CAS", "_WEU") }
                .map {
                    mapOf(
                        Pair("name", it.name),
                        Pair("value", it.value),
                        Pair("path", it.path),
                        Pair("domain", it.domain),
                    )
                }
            redisService.set(
                "spider:cookies",
                GsonUtil.toJson(cookies),
                30 * 60
            )
            cookies
        }
        logger.info("Cookies = {}", cookies)
        return cookies.map {
            Cookie.Builder()
                .name(it["name"]!!)
                .value(it["value"]!!)
                .path(it["path"]!!)
                .domain(it["domain"]!!)
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