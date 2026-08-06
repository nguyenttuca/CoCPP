from bisect import bisect_left, bisect_right
import sys

input = sys.stdin.readline

n, k = map(int, input().split())
a = list(map(int, input().split()))

c = list(set(a))
c.sort()
kq = 0
for i in range(n):
    a[i] = bisect_left(c,a[i]) + 1
cnt = [0]*(len(c) + 10)

cntpb = 0
def add_cnt(x):
    global cntpb
    if cnt[x] == 0:
        cntpb += 1
    cnt[x] += 1
def del_cnt(x):
    global cntpb
    if cnt[x] == 1:
        cntpb -= 1
    cnt[x] -= 1

ans = 0
l = 0
for r in range(n):
    add_cnt(a[r])
    while cntpb > k:
        del_cnt(a[l])
        l += 1
    ans += r - l + 1
    

print(ans)
