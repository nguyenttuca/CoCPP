from math import *
def uoc(n):
    cnt = 0
    for i in range(1,isqrt(n)+1):
        if n % i == 0:
            cnt = cnt + 1
            u = n // i
            if u != i:
                cnt = cnt + 1
    return(cnt)
d1 = int(input())
d2 = list(map(int, input().split()))
for k in range(d1):
    s = uoc(d2[k])
    print(s)
