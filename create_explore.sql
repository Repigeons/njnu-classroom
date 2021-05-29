SET NAMES utf8mb4;
use NjnuClassroom;

create table shuttle
(
    route         tinyint(1)                 not null comment '路线方向',
    start_time    varchar(5) default '00:00' not null comment '发车时间',
    start_station varchar(8)                 not null comment '起点站',
    end_station   varchar(8)                 not null comment '终点站',
    shuttle_count int                        not null comment '发车数量',
    working       bit(7)                     not null comment '工作日/双休日',
    primary key (route, start_time)
)   ENGINE = InnoDB
    DEFAULT CHARSET = utf8mb4
    comment '校车时刻表';

create index shuttle_working_route_start_time_index on shuttle (working, route, start_time);
