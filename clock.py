from sql import DDL_DB

def check_clock(time):
    DDL_DB.read_clock_by_time(time)