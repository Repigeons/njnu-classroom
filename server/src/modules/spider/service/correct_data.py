#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/7/1
# @Author   :  ZhouTianxing
# @Software :  PyCharm x64
""""""
from app import app
from orm import Correction
from ztxlib import aiomysql


async def correct():
    """
    从`correction`表读取数据，依此对`dev`表进行校正
    """
    mysql: aiomysql.MySQL = app['mysql']
    res = await mysql.fetchall("SELECT * FROM `correction`")
    correction_list = [Correction(row) for row in res]
    for correction in correction_list:
        # print([
        #     correction.day, correction.jc_ks, correction.jc_js,
        #     correction.JXLMC, correction.jsmph,
        #     correction.zylxdm, correction.jyytms, correction.kcm
        # ])
        data = [
            dict(
                day=correction.day,
                JASDM=correction.JASDM,
                jc=jc
            ) for jc in range(correction.jc_ks, correction.jc_js)
        ]
        if len(data) > 0:
            await mysql.execute(
                "DELETE FROM `dev` WHERE `day`=%(day)s AND `JASDM`=%(JASDM)s AND `jc_ks`=%(jc)s AND `jc_js`=%(jc)s",
                *data
            )
        await mysql.execute(
            "UPDATE `dev` SET "
            "`SKZWS`=%(skzws)s, "
            "`zylxdm`=%(zylxdm)s, "
            "`jc_ks`=%(jc_ks)s, "
            "`jyytms`=%(jyytms)s, "
            "`kcm`=%(kcm)s WHERE "
            "`day`=%(day)s AND "
            "`JASDM`=%(jasdm)s AND "
            "`jc_ks`=%(jc_js)s AND "
            "`jc_js`=%(jc_js)s",
            dict(
                skzws=correction.SKZWS,
                zylxdm=correction.zylxdm,
                jc_ks=correction.jc_ks,
                jc_js=correction.jc_js,
                jyytms=correction.jyytms,
                kcm=correction.kcm,
                day=correction.day,
                jasdm=correction.JASDM,
            )
        )


async def copy_to_dev() -> None:
    """
    将原始课程数据从`KCB`表复制到`dev`表，待后续处理
    """
    mysql: aiomysql.MySQL = app['mysql']
    await mysql.execute("TRUNCATE TABLE `dev`")
    await mysql.execute("INSERT INTO `dev` SELECT * FROM `KCB`")


async def copy_to_pro() -> None:
    """
    将课程数据从`dev`表复制到`pro`表，用于生产环境
    """
    mysql: aiomysql.MySQL = app['mysql']
    await mysql.execute("TRUNCATE TABLE `pro`")
    await mysql.execute("INSERT INTO `pro` SELECT * FROM `dev`")
