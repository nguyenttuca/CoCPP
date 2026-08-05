from bisect import *

n, m = map(int, input().split())
a = list(map(int, input().split()))
b = list(map(int, input().split()))

c = a + b
c.sort()
c = list(set(c))

for i in range(n):
    a[i] = bisect_left(c, a[i])

for i in range(m):
    b[i] = bisect_left(c, b[i])

cnta = [0] * 1000010
cntb = [0] * 1000010

for x in a:
    cnta[x] += 1
for x in b:
    cntb[x] += 1

for x in range(0, 400000):
    if cnta[x] > 0 and cntb[x] > 0:
        print(c[x], end = " ")
