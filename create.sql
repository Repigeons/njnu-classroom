SET NAMES utf8mb4;

create table JAS
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
    LC              tinyint          null comment '楼层',
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
    _SFYXZX         bit default b'0' not null comment '是否允许自习'
)   ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '教室列表';
create index JAS_JXLDM_index on JAS (JXLDM);

create table KCB
(
    id      int auto_increment primary key,
    JXLMC   varchar(32)                                                                         not null comment '教学楼名称',
    jsmph   varchar(32)                                                                         not null comment '教室门牌号',
    JASDM   char(10)                                                                            not null comment '教室代码',
    SKZWS   int                                                                                 not null comment '座位数',
    zylxdm  char(2) default '00'                                                                not null comment '类型代码',
    jc_ks   tinyint                                                                             not null comment '节次_开始',
    jc_js   tinyint                                                                             not null comment '节次_结束',
    jyytms  text                                                                                not null comment '借用用途说明',
    kcm     text                                                                                not null comment '课程名',
    day     enum ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday') not null comment '星期',
    _SFYXZX bit     default b'0'                                                                not null comment '是否允许自习'
)   ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '原始课程表';
create index kcb_day_index on KCB (day);
create index kcb_jasdm_index on KCB (JASDM);
create index kcb_jxl_index on KCB (JXLMC);

create table correction
(
    id      int auto_increment primary key,
    day     enum ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday') not null comment '星期',
    JXLMC   varchar(32)                                                                         not null comment '教学楼名称',
    jsmph   varchar(32)                                                                         not null comment '教室门牌号',
    JASDM   char(10)                                                                            not null comment '教室代码',
    SKZWS   int     default -1                                                                  not null comment '座位数',
    zylxdm  char(2) default '04'                                                                not null comment '类型代码',
    jc_ks   tinyint                                                                             not null comment '节次_开始',
    jc_js   tinyint                                                                             not null comment '节次_结束',
    jyytms  text                                                                                not null comment '借用用途说明',
    kcm     text                                                                                not null comment '课程名',
    _SFYXZX bit     default b'1'                                                                not null comment '是否允许自习'
)   ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '校正表';
create index correction_day_index on correction (day);
create index correction_jasdm_index on correction (JASDM);
create index correction_jxl_index on correction (JXLMC);

create table dev
(
    id      int auto_increment primary key,
    JXLMC   varchar(32)                                                                         not null comment '教学楼名称',
    jsmph   varchar(32)                                                                         not null comment '教室门牌号',
    JASDM   char(10)                                                                            not null comment '教室代码',
    SKZWS   int                                                                                 not null comment '座位数',
    zylxdm  char(2) default '00'                                                                not null comment '类型代码',
    jc_ks   tinyint                                                                             not null comment '节次_开始',
    jc_js   tinyint                                                                             not null comment '节次_结束',
    jyytms  text                                                                                not null comment '借用用途说明',
    kcm     text                                                                                not null comment '课程名',
    day     enum ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday') not null comment '星期',
    _SFYXZX bit     default b'0'                                                                not null comment '是否允许自习'
)   ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '开发环境';
create index dev_day_index on dev (day);
create index dev_jasdm_index on dev (JASDM);
create index dev_jxl_index on dev (JXLMC);

create table pro
(
    id      int auto_increment primary key,
    JXLMC   varchar(32)                                                                         not null comment '教学楼名称',
    jsmph   varchar(32)                                                                         not null comment '教室门牌号',
    JASDM   char(10)                                                                            not null comment '教室代码',
    SKZWS   int                                                                                 not null comment '座位数',
    zylxdm  char(2) default '00'                                                                not null comment '类型代码',
    jc_ks   tinyint                                                                             not null comment '节次_开始',
    jc_js   tinyint                                                                             not null comment '节次_结束',
    jyytms  text                                                                                not null comment '借用用途说明',
    kcm     text                                                                                not null comment '课程名',
    day     enum ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday') not null comment '星期',
    _SFYXZX bit     default b'0'                                                                not null comment '是否允许自习'
)   ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '生产环境';
create index pro_day_index on pro (day);
create index pro_jasdm_index on pro (JASDM);
create index pro_jxl_index on pro (JXLMC);

create table feedback_metadata
(
    id    int auto_increment primary key,
    time  timestamp default CURRENT_TIMESTAMP not null comment '日期',
    jc    int                                 not null comment '节次',
    JASDM char(10)                            not null comment '教室代码'
)   ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '用户反馈';

create view `feedback` as
    select `feedback_metadata`.`id`                            `id`,
           `JAS`.`JASMC`                                       `JASMC`,
           date_format(`feedback_metadata`.`time`, '%Y-%m-%d') `date`,
           date_format(`feedback_metadata`.`time`, '%W')       `day`,
           `feedback_metadata`.`jc`                            `jc`
    from `JAS`, `feedback_metadata`
    where `JAS`.`JASDM` = `feedback_metadata`.`JASDM`;
