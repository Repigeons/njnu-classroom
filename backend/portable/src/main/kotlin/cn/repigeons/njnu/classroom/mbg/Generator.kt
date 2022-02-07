package cn.repigeons.njnu.classroom.mbg

import org.mybatis.generator.api.MyBatisGenerator
import org.mybatis.generator.config.xml.ConfigurationParser
import org.mybatis.generator.internal.DefaultShellCallback

object Generator

/**
 * 用于生产MBG的代码
 */
fun main() {
    //MBG 执行过程中的警告信息
    val warnings = ArrayList<String>()
    //当生成的代码重复时，覆盖原代码
    val overwrite = true
    //读取我们的 MBG 配置文件
    val inputStream = Generator::class.java.getResourceAsStream("/generatorConfig.xml") ?: return
    val configurationParser = ConfigurationParser(warnings)
    val config = configurationParser.parseConfiguration(inputStream)
    inputStream.close()
    val callback = DefaultShellCallback(overwrite)
    //创建 MBG
    val myBatisGenerator = MyBatisGenerator(config, callback, warnings)
    //执行生成代码
    myBatisGenerator.generate(null)
    //输出警告信息
    for (warning in warnings) {
        println(warning)
    }
}