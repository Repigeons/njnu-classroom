SET NAMES utf8mb4;

create table sunday
(
    id       int auto_increment primary key,
    jsmph    varchar(32)          not null comment '教室门牌号',
    jxl      varchar(32)          not null comment '教学楼',
    jasdm    varchar(11)          not null comment '教室ID',
    capacity int                  not null comment '容纳人数',
    zylxdm   char(2) default '00' not null comment '类型代码',
    jc_ks    int                  not null comment '节次_开始',
    jc_js    int                  not null comment '节次_结束',
    jyytms   text                 not null comment '借用用途说明',
    kcm      text                 not null comment '课程名'
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '星期日';

create table monday
(
    id       int auto_increment primary key,
    jsmph    varchar(32)          not null comment '教室门牌号',
    jxl      varchar(32)          not null comment '教学楼',
    jasdm    varchar(11)          not null comment '教室ID',
    capacity int                  not null comment '容纳人数',
    zylxdm   char(2) default '00' not null comment '类型代码',
    jc_ks    int                  not null comment '节次_开始',
    jc_js    int                  not null comment '节次_结束',
    jyytms   text                 not null comment '借用用途说明',
    kcm      text                 not null comment '课程名'
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '星期一';

create table tuesday
(
    id       int auto_increment primary key,
    jsmph    varchar(32)          not null comment '教室门牌号',
    jxl      varchar(32)          not null comment '教学楼',
    jasdm    varchar(11)          not null comment '教室ID',
    capacity int                  not null comment '容纳人数',
    zylxdm   char(2) default '00' not null comment '类型代码',
    jc_ks    int                  not null comment '节次_开始',
    jc_js    int                  not null comment '节次_结束',
    jyytms   text                 not null comment '借用用途说明',
    kcm      text                 not null comment '课程名'
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '星期二';

create table wednesday
(
    id       int auto_increment primary key,
    jsmph    varchar(32)          not null comment '教室门牌号',
    jxl      varchar(32)          not null comment '教学楼',
    jasdm    varchar(11)          not null comment '教室ID',
    capacity int                  not null comment '容纳人数',
    zylxdm   char(2) default '00' not null comment '类型代码',
    jc_ks    int                  not null comment '节次_开始',
    jc_js    int                  not null comment '节次_结束',
    jyytms   text                 not null comment '借用用途说明',
    kcm      text                 not null comment '课程名'
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '星期三';

create table thursday
(
    id       int auto_increment primary key,
    jsmph    varchar(32)          not null comment '教室门牌号',
    jxl      varchar(32)          not null comment '教学楼',
    jasdm    varchar(11)          not null comment '教室ID',
    capacity int                  not null comment '容纳人数',
    zylxdm   char(2) default '00' not null comment '类型代码',
    jc_ks    int                  not null comment '节次_开始',
    jc_js    int                  not null comment '节次_结束',
    jyytms   text                 not null comment '借用用途说明',
    kcm      text                 not null comment '课程名'
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '星期四';

create table friday
(
    id       int auto_increment primary key,
    jsmph    varchar(32)          not null comment '教室门牌号',
    jxl      varchar(32)          not null comment '教学楼',
    jasdm    varchar(11)          not null comment '教室ID',
    capacity int                  not null comment '容纳人数',
    zylxdm   char(2) default '00' not null comment '类型代码',
    jc_ks    int                  not null comment '节次_开始',
    jc_js    int                  not null comment '节次_结束',
    jyytms   text                 not null comment '借用用途说明',
    kcm      text                 not null comment '课程名'
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '星期五';

create table saturday
(
    id       int auto_increment primary key,
    jsmph    varchar(32)          not null comment '教室门牌号',
    jxl      varchar(32)          not null comment '教学楼',
    jasdm    varchar(11)          not null comment '教室ID',
    capacity int                  not null comment '容纳人数',
    zylxdm   char(2) default '00' not null comment '类型代码',
    jc_ks    int                  not null comment '节次_开始',
    jc_js    int                  not null comment '节次_结束',
    jyytms   text                 not null comment '借用用途说明',
    kcm      text                 not null comment '课程名'
)
    ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '星期六';
