package cn.repigeons.njnu.classroom.service

import okhttp3.Cookie
import okhttp3.OkHttpClient

interface CookieService {
    fun getCookies(): List<Cookie>
    fun getHttpClient(cookies: List<Cookie>): OkHttpClient
}