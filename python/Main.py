#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# @Time     :  2020/05/30
# @Author   :  Zhou Tianxing
# @Software :  PyCharm Professional x64
# @FileName :  Main
""""""
import datetime
import json
import os
import shutil
import time
from json.decoder import JSONDecodeError

import get_data
import utils

# 预处理：初始化临时文件夹
temp_dir = '~tmp/'
None if os.path.exists(temp_dir) else os.mkdir(temp_dir)


def preparing() -> None:
    """
    准备工作
    收集cookie信息、时间信息和教学楼信息
    :return:None
    """

    # get cookies
    try:
        print('开始尝试获取cookies...')
        json.dump(
            utils.get_cookie_dict(account=json.load(open('conf/account.json'))),
            open(temp_dir + 'cookies.json', 'w')
        )
    except FileNotFoundError:
        print('配置文件缺失')
        print('Exit with code', 1)
        exit(1)
    except JSONDecodeError:
        print('配置文件解析失败')
        print('Exit with code', 1)
        exit(1)
    except KeyError:
        print('登录失败')
        print('Exit with code', 1)
        exit(1)
    except Exception as e:
        print(type(e), e)
        print('Exit with code', -1)
        exit(-1)
    cookies = json.load(open(temp_dir + 'cookies.json'))

    # get time related info  # （当前学年学期、周次、总周次、总教学周次）
    try:
        print('开始尝试查询时间信息...')
        json.dump(
            get_data.get_time_info(cookies=cookies),
            open(temp_dir + 'time_info.json', 'w')
        )
    except JSONDecodeError:
        print('cookies无效')
        print('Exit with code', 2)
        exit(2)
    except KeyError:
        print('获取时间信息失败')
        print('Exit with code', 3)
        exit(3)
    time_info = json.load(open(temp_dir + 'time_info.json'))

    # get jxl info
    try:
        print('开始尝试查询教学楼信息...')
        json.dump(
            get_data.get_jxl_info(
                cookies=cookies,
                xn_xq_dm=time_info['XNXQDM']
            ),
            open(temp_dir + 'jxl_info.json', 'w', encoding='utf8'),
            ensure_ascii=False
        )
    except JSONDecodeError:
        print('cookies无效')
        print('Exit with code', 2)
        exit(2)
    except KeyError:
        print('获取教学楼信息失败')
        print('Exit with code', 3)
        exit(3)
    jxl_info = json.load(open(temp_dir + 'jxl_info.json', encoding='utf8'))

    # get classroom info
    try:
        classrooms = []
        for jxl in jxl_info:
            classroom_info = get_data.get_classroom_info(
                cookies=cookies,
                xn_xq_dm=time_info['XNXQDM'],
                jxl_dm=jxl['JXLDM']
            )
            classrooms.extend(classroom_info)
            json.dump(
                classroom_info,
                open(temp_dir + f"classroom_info_{jxl['JXLMC']}.json", 'w', encoding='utf8'),
                ensure_ascii=False
            )

        # save classrooms info to static directory
        try:
            config = json.load(open('conf/config.json'))
            utils.dump_static_json(
                classrooms=classrooms,
                filename=f"{config['staticPath']}/classrooms.json"
            )
        except FileNotFoundError:
            print('配置文件缺失')
            print('Exit with code', 1)
            exit(1)
        except JSONDecodeError:
            print('配置文件解析失败')
            print('Exit with code', 1)
            exit(1)
    except JSONDecodeError:
        print('cookies无效')
        print('Exit with code', 2)
        exit(2)
    except KeyError:
        print('获取教室信息失败')
        print('Exit with code', 3)
        exit(3)


def core() -> None:
    """
    核心任务
    收集各教室在各时间段的数据，并存入数据库
    :return:None
    """

    utils.truncate()
    # load stored info
    cookies = json.load(open(temp_dir + 'cookies.json'))
    time_info = json.load(open(temp_dir + 'time_info.json'))
    jxl_info = json.load(open(temp_dir + 'jxl_info.json', encoding='utf8'))

    # get class info
    try:
        for jxl in jxl_info:
            classroom_info = json.load(open(temp_dir + 'classroom_info_%s.json' % jxl['JXLMC'], encoding='utf8'))
            print('开始查询教学楼:', jxl['JXLMC'])
            for classroom in classroom_info:
                classroom['jsmph'] = classroom['JASMC'].replace(classroom['JXLMC'], '')
                print('正在查询教室:', classroom['JASMC'])
                class_info = get_data.get_class_weekly(
                    cookies=cookies,
                    xn_xq_dm=time_info['XNXQDM'],
                    jas_dm=classroom['JASDM'],
                    zc=time_info['ZC'],
                    zzc=time_info['ZZC']
                )
                for weekday in range(7):
                    args_list = []
                    for data in class_info[weekday]:
                        print([
                            classroom['jsmph'],
                            classroom['JXLMC'],
                            classroom['JASDM'],
                            classroom['SKZWS'],
                            data['ZYLXDM'],
                            data['JC'][0],
                            data['JC'][1],
                            data['JYYTMS'],
                            data['KCM']
                        ])
                        args_list.append({
                            'jsmph': classroom['jsmph'],
                            'jxl': classroom['JXLMC'],
                            'jasdm': classroom['JASDM'],
                            'capacity': classroom['SKZWS'],
                            'zylxdm': data['ZYLXDM'],
                            'jc_ks': data['JC'][0],
                            'jc_js': data['JC'][1],
                            'jyytms': data['JYYTMS'],
                            'kcm': data['KCM']
                        })
                    utils.insert(weekday, args_list)
    except JSONDecodeError:
        print('cookies无效')
        print('Exit with code', 2)
        exit(2)
    except Exception as e:
        print(type(e), e)
        print('Exit with code', -1)
        exit(-1)


# 主函数
if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-env', default='dev', type=str, help='developing environment or production environment')
    args = parser.parse_args()

    # Runnable main
    preparing()

    print('基础信息采集完成')
    print('即将开始采集详细信息')
    time.sleep(10)

    core()

    if args.env == 'pro':
        utils.save_to_pro()

    print()
    print('--------------------------------------------------')
    print(datetime.datetime.now().strftime('[%Y-%m-%d %X]'), '本轮具体课程信息收集工作成功完成。')
    print()

# 收尾：清理临时文件夹
shutil.rmtree(temp_dir)
exit(0)
