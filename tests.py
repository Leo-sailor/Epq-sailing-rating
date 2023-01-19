import time as t
def timeslow(length):
    starttime = t.perf_counter_ns()
    long = range(0,length)
    for item in long:
        print(item)
    endtime = t.perf_counter_ns()
    return endtime - starttime
def timefast(length):
    starttime = t.perf_counter_ns()
    long = list(range(0,length))
    for x in range(length):
        long[x] = str(long[x])
    print('\n'.join(long))
    endtime = t.perf_counter_ns()
    print(type(endtime))
    return endtime - starttime
x = timefast(1000)
y = timeslow(1000)
print(f'Fast took: {x}')
print(f'Slow took: {y}')
t.sleep(10)
