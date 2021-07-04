#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# @Time     :  2021/1/10 0010
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  _correct_data.py
""""""
from App.Spider import dao


async def correct() -> None:
    """
    从`correction`表读取数据，依此对`dev`表进行校正
    """
    print("待校正数据：")
    correction_list = dao.get_correction()
    for correction in correction_list:
        print([
            correction.day, correction.jc_ks, correction.jc_js,
            correction.JXLMC, correction.jsmph,
            correction.zylxdm, correction.jyytms, correction.kcm
        ])
        data = [
            {'day': correction.day, 'JASDM': correction.JASDM, 'jc': jc}
            for jc in range(correction.jc_ks, correction.jc_js)
        ]
        if len(data) > 0:
            dao.delete_incorrectness(*data)
        dao.update_incorrectness(
            skzws=correction.SKZWS,
            zylxdm=correction.zylxdm,
            jc_ks=correction.jc_ks,
            jc_js=correction.jc_js,
            jyytms=correction.jyytms,
            kcm=correction.kcm,
            day=correction.day,
            jasdm=correction.JASDM,
        )


def copy_to_dev() -> None:
    """
    将原始课程数据从`KCB`表复制到`dev`表，待后续处理
    """
    dao.truncate_dev()
    dao.copy_kcb_to_dev()


def copy_to_pro() -> None:
    """
    将课程数据从`dev`表复制到`pro`表，用于生产环境
    """
    dao.truncate_pro()
    dao.copy_dev_to_pro()
