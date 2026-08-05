from bisect import *

n = int(input())
a = list(map(int, input().split()))

a.sort()
comp = list(set(a))
comp.sort()

cnt = [0] * 1000010

for x in a:
    i = bisect_left(comp, x)
    cnt[i] += 1

for i in range(len(comp)):
    if cnt[i] > 0:
        print(comp[i], cnt[i], end = " ")
        print()
