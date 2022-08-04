package cn.repigeons.njnu.classroom

import org.junit.jupiter.api.Assertions
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test
import org.openqa.selenium.WebDriver
import org.openqa.selenium.chrome.ChromeDriver
import org.openqa.selenium.chrome.ChromeOptions

class SeleniumTests {
    private lateinit var driver: WebDriver

    @BeforeEach
    fun init() {
        val options = ChromeOptions()
        options.setExperimentalOption("debuggerAddress", "127.0.0.1:9222")
        driver = ChromeDriver(options)
    }

    @Test
    fun testBaidu() {
        driver.get("https://baidu.com")
        Assertions.assertEquals("https://www.baidu.com/", driver.currentUrl)
    }

    @Test
    fun testBing() {
        driver.get("https://bing.com")
        Assertions.assertEquals("https://cn.bing.com/", driver.currentUrl)
    }
}