from bisect import *
n = int(input())
a = list(map(int, input().split()))
a.sort()
c = list(set(a))
c.sort()
for i in range(n):
    a[i] = bisect_left(c,a[i])
cnt = [0]*len(c)

Ans = 0
for i in range(n):
    Ans = Ans + cnt[a[i]]
    cnt[a[i]] += 1

print(Ans)
