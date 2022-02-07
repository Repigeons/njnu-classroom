package cn.repigeons.njnu.classroom.service.impl

import cn.repigeons.njnu.classroom.service.CookieService
import cn.repigeons.njnu.classroom.service.RedisService
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import okhttp3.Cookie
import okhttp3.CookieJar
import okhttp3.HttpUrl
import okhttp3.OkHttpClient
import org.openqa.selenium.By
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions
import org.openqa.selenium.firefox.FirefoxDriver
import org.openqa.selenium.firefox.FirefoxOptions
import org.slf4j.LoggerFactory
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service

@Service
class CookieServiceImpl(
    private val gson: Gson,
    private val redisService: RedisService,
    @Value("\${selenium.driver}") private val driver: String,
    @Value("\${selenium.firefox.exec_path:}") firefox: String?,
    @Value("\${selenium.firefox.geckodriver:}") geckodriver: String?,
    @Value("\${account.username}") private val username: String,
    @Value("\${account.password}") private val password: String,
    @Value("\${account.gid}") private val gid: String,
) : CookieService {
    private val logger = LoggerFactory.getLogger(javaClass)
    private val firefoxOptions = FirefoxOptions()
    private val chromeOptions = ChromeOptions()

    init {
        System.getProperties().setProperty("webdriver.gecko.driver", geckodriver)
        firefoxOptions.setBinary(firefox)
        firefoxOptions.addArguments("-headless")
        chromeOptions.addArguments("--headless", "--no-sandbox", "--disable-dev-shm-usage")
    }

    override fun getCookies(): List<Cookie> {
        val cookies = redisService["spider:cookies"]
            ?.let {
                gson.fromJson(it, object : TypeToken<List<Map<String, String>>>() {}.type)
            }
            ?: let {
                val webDriver: WebDriver = when (driver) {
                    "chromium" -> ChromeDriver(chromeOptions)
                    "firefox" -> FirefoxDriver(firefoxOptions)
                    else -> throw IllegalArgumentException()
                }
                webDriver.get("http://ehallapp.nnu.edu.cn/jwapp/sys/jsjy/*default/index.do?amp_sec_version_=1&gid_=$gid")
                Thread.sleep(5000)
                webDriver.switchTo().defaultContent()
                webDriver.findElement(By.id("username")).sendKeys(username)
                webDriver.findElement(By.id("password")).sendKeys(password)
                webDriver.findElement(By.id("login_submit")).click()
                val cookies = webDriver.manage().cookies
                    .filter { it.name in listOf("MOD_AUTH_CAS", "_WEU") }
                    .map {
                        mapOf(
                            Pair("name", it.name),
                            Pair("value", it.value),
                            Pair("path", it.path),
                            Pair("domain", it.domain),
                        )
                    }
                webDriver.quit()
                redisService.set(
                    "spider:cookies",
                    gson.toJson(cookies),
                    30 * 60 * 1000
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