"""
Generator cho bài "Con đường" (ROAD.INP / ROAD.OUT)
- Cập nhật Subtask 3: N lên tới 10^6.
- Đã tối ưu tốc độ sinh mảng và phân tích thừa số trong Python để sinh mảng triệu phần tử siêu tốc.
"""

import random
import sys
import os
from collections import deque

MAXA = 10 ** 6
sys.set_int_max_str_digits(0)

# ---------------------------------------------------------------------------
# Sàng nguyên tố nhỏ nhất (SPF) tới 10^6, dùng để phân tích thừa số nhanh
# ---------------------------------------------------------------------------
def sieve_spf(maxv):
    spf = list(range(maxv + 1))
    i = 2
    while i * i <= maxv:
        if spf[i] == i:
            for j in range(i * i, maxv + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1
    return spf

SPF = sieve_spf(MAXA)

def prime_factors(x):
    fs = set()
    while x > 1:
        p = SPF[x]
        fs.add(p)
        while x % p == 0:
            x //= p
    return fs

def primes_up_to(m):
    if m < 2:
        return []
    sieve = bytearray([1]) * (m + 1)
    sieve[0] = sieve[1] = 0
    for i in range(2, int(m ** 0.5) + 1):
        if sieve[i]:
            sieve[i * i::i] = bytearray(len(range(i * i, m + 1, i)))
    return [i for i, v in enumerate(sieve) if v]

# ---------------------------------------------------------------------------
# Solver chuẩn (Python) dùng để tự động kiểm tra đáp án
# ---------------------------------------------------------------------------
def solve(A):
    n = len(A)
    prime_id = {}
    node_adj = [[] for _ in range(n)]
    prime_adj = []

    for i, a in enumerate(A):
        for p in prime_factors(a):
            pid = prime_id.get(p)
            if pid is None:
                pid = n + len(prime_id)
                prime_id[p] = pid
                prime_adj.append([])
            node_adj[i].append(pid)
            prime_adj[pid - n].append(i)

    total = n + len(prime_id)
    dist = [-1] * total
    dist[0] = 0
    dq = deque([0])
    while dq:
        u = dq.popleft()
        neigh = node_adj[u] if u < n else prime_adj[u - n]
        du1 = dist[u] + 1
        for v in neigh:
            if dist[v] == -1:
                dist[v] = du1
                dq.append(v)

    d = dist[n - 1]
    return -1 if d == -1 else d // 2

def max_achievable_hops(maxA, n=None):
    limit = int(maxA ** 0.5) + 2
    plist = primes_up_to(limit)
    if len(plist) < 2: return 0
    m = 1
    while m < len(plist) and plist[m - 1] * plist[m] <= maxA:
        m += 1
    cap = m - 1
    if n is not None: cap = min(cap, n - 1)
    return cap

def gen_forced_chain(n, maxA, rnd):
    limit = int(maxA ** 0.5) + 2
    plist = primes_up_to(limit)
    m = 1
    while m < len(plist) and plist[m - 1] * plist[m] <= maxA: m += 1
    plist = plist[:m]
    if len(plist) > n: plist = plist[:n]
    chain_vals = [plist[0]]
    for i in range(1, len(plist)):
        chain_vals.append(plist[i - 1] * plist[i])
    k = len(chain_vals)
    positions = [1 + round(i * (n - 1) / (k - 1)) for i in range(k)]
    for i in range(1, k):
        if positions[i] <= positions[i - 1]: positions[i] = positions[i - 1] + 1
    positions[-1] = n
    for i in range(k - 2, -1, -1):
        if positions[i] >= positions[i + 1]: positions[i] = positions[i + 1] - 1
    A = [1] * (n + 1)
    for pos, v in zip(positions, chain_vals): A[pos] = v
    return A[1:], k - 1, set(plist)

def add_controlled_noise(A, maxA, rnd, pool, chain_primes):
    n = len(A)
    pool = [p for p in pool if p not in chain_primes]
    if not pool: return A
    for i in range(n):
        if A[i] != 1: continue
        if rnd.random() < 0.35:
            k = rnd.choice([1, 2, 2, 3])
            cand = rnd.sample(pool, min(len(pool), max(k, 4)))
            prod, chosen = 1, 0
            for p in cand:
                if prod * p <= maxA:
                    prod *= p
                    chosen += 1
                    if chosen >= k: break
            if prod > 1: A[i] = prod
    return A

def generate_until_ok(n, maxA, target_ratio=1/3, max_tries=200, seed_base=0):
    theoretical_cap = max_achievable_hops(maxA, n)
    threshold = max(1, round(n * target_ratio))
    threshold = min(threshold, max(1, theoretical_cap - 1))
    noise_pool_full = primes_up_to(min(2000, maxA))

    for attempt in range(max_tries):
        rnd = random.Random(seed_base + attempt)
        A, expected, chain_primes = gen_forced_chain(n, maxA, rnd)
        A = add_controlled_noise(A, maxA, rnd, noise_pool_full, chain_primes)
        ans = solve(A)
        if ans != -1 and ans >= threshold:
            return A, ans
    raise RuntimeError("Failed to generate suitable test for sub 1/2.")

# ---------------------------------------------------------------------------
# SINH TEST ĐẶC BIỆT CHO SUBTASK 3 NHẰM KILL CODE CỦA SUB 2 (N = 10^6)
# Đã được tối ưu tốc độ mảng (array operations) cho Python
# ---------------------------------------------------------------------------
def generate_sub3_exact(n, target_ans, seed):
    rnd = random.Random(seed)
    
    # 1. Tạo chuỗi đúng 'target_ans' bước bằng các nguyên tố nhỏ
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    chain_primes = small_primes[:target_ans]
    
    chain_vals = [chain_primes[0]]
    for i in range(1, target_ans):
        chain_vals.append(chain_primes[i-1] * chain_primes[i])
    chain_vals.append(chain_primes[-1])
    
    # 2. Chuẩn bị "bể dữ liệu nhiễu" để làm TLE/RTE code yếu
    large_primes = [p for p in primes_up_to(10**6) if 500000 < p <= 1000000]
    mid_primes = [p for p in primes_up_to(1000) if p > 900]
    
    # Tạo trước 1 pool chứa trộn lẫn các giá trị độc (tránh for lặp trong Python)
    noise_pool = rnd.sample(large_primes, 200) # Lấy 200 nguyên tố lớn
    
    # Thêm các tích 2 nguyên tố gần 1000
    for _ in range(200):
        p1 = rnd.choice(mid_primes)
        p2 = rnd.choice(mid_primes)
        if p1 * p2 <= 10**6:
            noise_pool.append(p1 * p2)
            
    # Random.choices được viết bằng C, sinh ra mảng 1 triệu phần tử siêu tốc
    A = rnd.choices(noise_pool, k=n)
    
    # 3. Ghi đè đường đi chuẩn xác vào mảng
    positions = [0] + sorted(rnd.sample(range(1, n - 1), target_ans - 1)) + [n - 1]
    for pos, val in zip(positions, chain_vals):
        A[pos] = val
        
    return A

OUT_DIR = "road_tests"
os.makedirs(OUT_DIR, exist_ok=True)

def write_test(path_in, A):
    n = len(A)
    with open(path_in, "w") as f:
        f.write(f"{n}\n")
        f.write(" ".join(map(str, A)) + "\n")

def write_output(path_out, answer):
    with open(path_out, "w") as f:
        f.write(f"{answer}\n")

if __name__ == "__main__":
    PLAN_1_2 = [
        # ---- Subtask 1: n <= 1000, A_i <= 10^6 (6 test) ----
        (1,   50, 10**6,  101),
        (1,  200, 10**6,  102),
        (1,  500, 10**6,  103),
        (1,  800, 10**6,  104),
        (1, 1000, 10**6,  105),
        (1, 1000, 10**6,  106),

        # ---- Subtask 2: n <= 10^5, A_i <= 1000 (6 test) ----
        (2,   1000, 1000, 201),
        (2,  10000, 1000, 202),
        (2,  30000, 1000, 203),
        (2,  60000, 1000, 204),
        (2,  90000, 1000, 205),
        (2, 100000, 1000, 206),
    ]

    # ---- Subtask 3: n <= 10^6, A_i <= 10^6 (8 test riêng biệt) ----
    PLAN_3 = [
        (3,  930000, 10**6, 301, 3),
        (3,  940000, 10**6, 302, 4),
        (3,  950000, 10**6, 303, 5),
        (3,  960000, 10**6, 304, 6),
        (3,  970000, 10**6, 305, 7),
        (3,  980000, 10**6, 306, 8),
        (3,  990000, 10**6, 307, 9),
        (3, 1000000, 10**6, 308, 10),
    ]

    counters = {1: 0, 2: 0, 3: 0}
    summary = []
    
    # Sinh Sub 1 và Sub 2
    for sub, n, maxA, seed in PLAN_1_2:
        counters[sub] += 1
        A, ans = generate_until_ok(n=n, maxA=maxA, target_ratio=1/3, seed_base=seed)
        base = f"ROAD_sub{sub}_test{counters[sub]:02d}"
        write_test(os.path.join(OUT_DIR, base + ".INP"), A)
        write_output(os.path.join(OUT_DIR, base + ".OUT"), ans)
        summary.append((base, n, maxA, ans))

    # Sinh Sub 3 (Sử dụng hàm đã tối ưu tốc độ sinh mảng triệu phần tử)
    print("\nĐang sinh Sub 3 (N=10^6), thuật toán BFS Python có thể mất vài giây mỗi test, vui lòng đợi...")
    for sub, n, maxA, seed, target_ans in PLAN_3:
        counters[sub] += 1
        A = generate_sub3_exact(n=n, target_ans=target_ans, seed=seed)
        ans = solve(A)
        assert ans == target_ans, f"Lỗi sinh Sub 3: Kỳ vọng {target_ans} nhưng thực tế BFS ra {ans}"
        
        base = f"ROAD_sub{sub}_test{counters[sub]:02d}"
        write_test(os.path.join(OUT_DIR, base + ".INP"), A)
        write_output(os.path.join(OUT_DIR, base + ".OUT"), ans)
        summary.append((base, n, maxA, ans))

    print("\n==== TỔNG KẾT ====")
    for base, n, maxA, ans in summary:
        print(f"{base:28s} n={n:<7} maxA={maxA:<9} answer={ans}")
    print(f"\nĐã sinh {len(summary)} test tại: {os.path.abspath(OUT_DIR)}")