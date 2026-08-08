from math import *
n = int(input())
a = list(map(int,input().split()))
mx = int(max(a))
cnt = [0]*(mx+100)

for k in range(1,mx+1):
    for j in range(k,mx+1,k):
        cnt[j] = cnt[j] + 1
for i in range(n):
    print(cnt[a[i]])
