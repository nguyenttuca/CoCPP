from bisect import *

n, k = map(int, input().split())
x = [0]
for _ in range(n):
    x.append(int(input()))

x.sort()

def check(dist):
    i = 1
    cnt = 1
    while i < n:
        j = bisect_left(x, dist + x[i])
        if j == len(x):
            if cnt == k:
                return 1
            else:
                return 0
        else:
            i = j 
            cnt += 1
            if cnt == k:
                return 1
    
    if cnt == k:
        return 1
    else:
        return 0

l, r = 1, 1000000000000000000
AnsMax = -float('inf')

while l <= r:
    mid = (l + r) // 2
    if check(mid) == 1:
        AnsMax = mid
        l = mid + 1
    else:
        r = mid - 1

print(AnsMax)
