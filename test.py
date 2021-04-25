import time

while 1:
    now = time.localtime( time.time() )
    if  now.tm_sec==0:
        print(time.asctime(now))