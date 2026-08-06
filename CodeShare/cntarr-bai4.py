from bisect import bisect_left, bisect_right
import sys

input = sys.stdin.readline

n, q = map(int, input().split())
a = list(map(int, input().split()))
a.sort()

c = list(set(a))
c.sort()
kq = 0
for i in range(n):
    a[i] = bisect_left(c,a[i]) + 1
cnt = [0]*(len(c) + 10)
for x in a:
    cnt[x] = cnt[x] + 1

pre = [0] * (len(c) + 10)
for i in range(1, len(c) + 9):
    pre[i] = pre[i - 1] + cnt[i]

ans = []
for _ in range(q):
    l, r = map(int, input().split())
    r = bisect_right(c, r)
    l = bisect_left(c, l)
    ans.append(str(pre[r] - pre[l]))

sys.stdout.write("\n".join(ans))
