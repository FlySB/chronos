import time

def time_t(a):
    timeArray = time.strptime(a,"%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp