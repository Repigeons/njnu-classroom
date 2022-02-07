create table if not exists JAS
(
    JASDM           char(10)         not null comment '教室代码' primary key,
    JASMC           varchar(32)      not null comment '教室名称',
    JXLDM           varchar(8)       not null comment '教学楼代码',
    JXLDM_DISPLAY   varchar(16)      not null comment '教学楼名称',
    XXXQDM          varchar(4)       not null comment '学校校区代码',
    XXXQDM_DISPLAY  varchar(16)      not null comment '学校校区名称',
    JASLXDM         varchar(8)       null comment '教室类型代码',
    JASLXDM_DISPLAY varchar(16)      null comment '教室类型名称',
    ZT              varchar(8)       null comment '状态',
    LC              smallint(1)      null comment '楼层',
    JSYT            text             null comment '教室用途',
    SKZWS           int              not null comment '上课座位数',
    KSZWS           int              not null comment '考试座位数',
    XNXQDM          varchar(32)      null comment '学年学期代码',
    XNXQDM2         varchar(32)      null comment '学年学期代码2',
    DWDM            varchar(32)      null comment '管理单位代码',
    DWDM_DISPLAY    varchar(32)      null comment '管理单位名称',
    ZWSXDM          varchar(8)       null comment '座位属性代码',
    XGDD            text             null comment '相关地点',
    SYRQ            varchar(32)      null comment '使用日期',
    SYSJ            varchar(32)      null comment '使用时间',
    SXLB            varchar(32)      null comment '实习类别',
    BZ              text             null comment '备注',
    SFYPK           bit              null comment '是否已排课',
    SFYXPK          bit              null comment '是否允许排课',
    PKYXJ           varchar(32)      null comment '排课优先级',
    SFKSWH          bit              null comment '是否考试维护',
    SFYXKS          bit              null comment '是否允许考试',
    KSYXJ           varchar(32)      null comment '考试优先级',
    SFYXCX          bit              null comment '是否允许查询',
    SFYXJY          bit              null comment '是否允许借用',
    SFYXZX          bit default b'0' not null comment '是否允许自习'
)
    comment '教室列表';
create index if not exists JAS_JXLDM_index on JAS (JXLDM);

create table if not exists KCB
(
    id     int auto_increment primary key,
    JXLMC  varchar(32)                                                   not null comment '教学楼名称',
    jsmph  varchar(32)                                                   not null comment '教室门牌号',
    JASDM  char(10)                                                      not null comment '教室代码',
    SKZWS  int                                                           not null comment '座位数',
    zylxdm char(2) default '00'                                          not null comment '类型代码',
    jc_ks  smallint(2)                                                   not null comment '节次_开始',
    jc_js  smallint(2)                                                   not null comment '节次_结束',
    jyytms text                                                          not null comment '借用用途说明',
    kcm    text                                                          not null comment '课程名',
    day    enum ('Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.') not null comment '星期',
    SFYXZX bit     default b'0'                                          not null comment '是否允许自习'
)
    comment '原始课程表';
create index if not exists kcb_day_index on KCB (day);
create index if not exists kcb_jasdm_index on KCB (JASDM);
create index if not exists kcb_jxl_index on KCB (JXLMC);

create table if not exists correction
(
    id     int auto_increment primary key,
    day    enum ('Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.') not null comment '星期',
    JXLMC  varchar(32)                                                   not null comment '教学楼名称',
    jsmph  varchar(32)                                                   not null comment '教室门牌号',
    JASDM  varchar(10)                                                   not null comment '教室代码',
    SKZWS  int        default -1                                         not null comment '座位数',
    zylxdm varchar(2) default '04'                                       not null comment '类型代码',
    jc_ks  smallint(2)                                                   not null comment '节次_开始',
    jc_js  smallint(2)                                                   not null comment '节次_结束',
    jyytms text                                                          not null comment '借用用途说明',
    kcm    text                                                          not null comment '课程名',
    SFYXZX bit        default b'1'                                       not null comment '是否允许自习'
)
    comment '校正表';
create index if not exists correction_day_index on correction (day);
create index if not exists correction_jasdm_index on correction (JASDM);
create index if not exists correction_jxl_index on correction (JXLMC);

create table if not exists dev
(
    id     int auto_increment primary key,
    JXLMC  varchar(32)                                                   not null comment '教学楼名称',
    jsmph  varchar(32)                                                   not null comment '教室门牌号',
    JASDM  char(10)                                                      not null comment '教室代码',
    SKZWS  int                                                           not null comment '座位数',
    zylxdm char(2) default '00'                                          not null comment '类型代码',
    jc_ks  smallint(2)                                                   not null comment '节次_开始',
    jc_js  smallint(2)                                                   not null comment '节次_结束',
    jyytms text                                                          not null comment '借用用途说明',
    kcm    text                                                          not null comment '课程名',
    day    enum ('Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.') not null comment '星期',
    SFYXZX bit     default b'0'                                          not null comment '是否允许自习'
)
    comment '开发环境';
create index if not exists dev_day_index on dev (day);
create index if not exists dev_jasdm_index on dev (JASDM);
create index if not exists dev_jxl_index on dev (JXLMC);

create table if not exists feedback_metadata
(
    id    int auto_increment primary key,
    time  timestamp default current_timestamp() not null comment '日期',
    jc    smallint(2)                           not null comment '节次',
    JASDM char(10)                              not null comment '教室代码'
)
    comment '用户反馈';

create table if not exists notice
(
    id   int auto_increment primary key,
    time timestamp default current_timestamp() not null on update current_timestamp() comment '发布时间',
    text varchar(1024)                         not null comment '公告内容'
)
    comment '公告记录';

create table if not exists pro
(
    id     int auto_increment primary key,
    JXLMC  varchar(32)                                                   not null comment '教学楼名称',
    jsmph  varchar(32)                                                   not null comment '教室门牌号',
    JASDM  char(10)                                                      not null comment '教室代码',
    SKZWS  int                                                           not null comment '座位数',
    zylxdm char(2) default '00'                                          not null comment '类型代码',
    jc_ks  smallint(2)                                                   not null comment '节次_开始',
    jc_js  smallint(2)                                                   not null comment '节次_结束',
    jyytms text                                                          not null comment '借用用途说明',
    kcm    text                                                          not null comment '课程名',
    day    enum ('Sun.', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.') not null,
    SFYXZX bit     default b'0'                                          not null comment '是否允许自习'
)
    comment '生产环境';
create index if not exists pro_day_index on pro (day);
create index if not exists pro_jasdm_index on pro (JASDM);
create index if not exists pro_jxl_index on pro (JXLMC);

create table if not exists shuttle
(
    route         smallint(1)                not null comment '路线方向',
    start_time    varchar(5) default '00:00' not null comment '发车时间',
    start_station varchar(8)                 not null comment '起点站',
    end_station   varchar(8)                 not null comment '终点站',
    shuttle_count int                        not null comment '发车数量',
    working       bit(7)                     not null comment '工作日/双休日',
    primary key (route, start_time)
)
    comment '校车时刻表';
create index if not exists shuttle_working_route_start_time_index on shuttle (working, route, start_time);
