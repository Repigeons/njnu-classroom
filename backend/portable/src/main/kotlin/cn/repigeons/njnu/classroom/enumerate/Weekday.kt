package cn.repigeons.njnu.classroom.enumerate

enum class Weekday {
    Mon, Tue, Wed, Thu, Fri, Sat, Sun;

    companion object {
        operator fun get(index: Int) = values()[index]
    }
}