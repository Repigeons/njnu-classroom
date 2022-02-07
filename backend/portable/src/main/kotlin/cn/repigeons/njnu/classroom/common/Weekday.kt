package cn.repigeons.njnu.classroom.common

enum class Weekday(val value: String) {
    Monday("Mon."),
    Tuesday("Tue."),
    Wednesday("Wed."),
    Thursday("Thu."),
    Friday("Fri."),
    Saturday("Sat."),
    Sunday("Sun.");

    companion object {
        fun parse(value: String) = values().firstOrNull { it.value == value }
    }
}