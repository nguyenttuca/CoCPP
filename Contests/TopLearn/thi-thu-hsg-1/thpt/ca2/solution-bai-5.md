# Lời giải chi tiết: Bài 5 - Con đường (ROAD)

## 1. Tóm tắt đề bài
- Cho một mảng `A` gồm `n` phần tử, người chơi xuất phát từ vị trí `1` và cần đi đến vị trí `n`.
- Từ vị trí `i`, chỉ có thể nhảy đến vị trí `j` nếu:
  1. Tiến về phía trước: `i < j`.
  2. Năng lượng tương thích: `gcd(A[i], A[j]) > 1`.
- **Yêu cầu:** Tìm số bước nhảy ít nhất để đi từ `1` đến `n`. Nếu không thể đến đích, in ra `-1`.

## 2. Phân tích chung
Bài toán yêu cầu tìm "số bước ít nhất", đây là dấu hiệu đặc trưng của lớp bài toán **Tìm đường đi ngắn nhất trên đồ thị không trọng số** (giải bằng BFS) hoặc **Quy hoạch động (DP)**.
Nhờ điều kiện bắt buộc phải đi tới (`i < j`), đồ thị sinh ra sẽ không có chu trình (DAG - Directed Acyclic Graph). Do đó, bài toán này có thể được giải trọn vẹn bằng cả hai phương pháp.

---

## 3. Lời giải chi tiết và Cài đặt (Theo hướng Quy hoạch động)

### Subtask 1: Thuật toán ngây thơ - `O(N^2)`
**Giới hạn:** `n <= 1000`, `A[i] <= 10^6`.

*   **Định nghĩa:** Gọi `dp[i]` là số bước nhảy ít nhất để đi từ ô `1` đến ô `i`. Khởi tạo `dp[1] = 0`, các ô khác bằng vô cực (`+INF`).
*   **Công thức truy hồi:** 
    Để tính `dp[j]`, ta duyệt qua tất cả các ô `i` đứng trước nó (`1 <= i < j`). Nếu từ `i` có thể nhảy đến `j` (tức là `gcd(A[i], A[j]) > 1`), ta cập nhật:
    
    `dp[j] = min(dp[j], dp[i] + 1)`

*   **Đánh giá:** Hai vòng lặp lồng nhau mất `O(N^2)` phép tính. Chạy tốt với `n <= 1000`.

**Code C++:**
```cpp
#include <bits/stdc++.h>

using namespace std;

const int INF = 1e9;
int a[1005];
int dp[1005];

int gcd(int x, int y) {
    while (y != 0) {
        int t = y;
        y = x % y;
        x = t;
    }
    return x;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    freopen("road.inp", "r", stdin);
    freopen("road.out", "w", stdout);

    int n;
    if (!(cin >> n)) return 0;
    
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    for (int i = 1; i <= n; i++) dp[i] = INF;
    dp[1] = 0;

    for (int i = 1; i <= n; i++) {
        if (dp[i] == INF) continue;
        for (int j = i + 1; j <= n; j++) {
            if (gcd(a[i], a[j]) > 1) {
                dp[j] = min(dp[j], dp[i] + 1);
            }
        }
    }

    if (dp[n] == INF) cout << -1 << "\n";
    else cout << dp[n] << "\n";

    return 0;
}
```

**Code Python:**
```python
import sys
import math

def solve():
    sys.stdin = open('road.inp', 'r')
    sys.stdout = open('road.out', 'w')
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [0] + [int(x) for x in input_data[1:n+1]]
    
    INF = float('inf')
    dp = [INF] * (n + 1)
    dp[1] = 0
    
    for i in range(1, n + 1):
        if dp[i] == INF:
            continue
        for j in range(i + 1, n + 1):
            if math.gcd(a[i], a[j]) > 1:
                dp[j] = min(dp[j], dp[i] + 1)
                
    print(dp[n] if dp[n] != INF else -1)

if __name__ == '__main__':
    solve()
```

---

### Subtask 2: Tối ưu với không gian giá trị nhỏ - `O(N * sqrt(A[i]))`
**Giới hạn:** `n <= 10^5`, `A[i] <= 1000`.

Hai số có `gcd > 1` khi và chỉ khi chúng **có chung ít nhất một thừa số nguyên tố**. Ta không cần duyệt lại toàn bộ các ô phía trước.
*   **Cải tiến trạng thái:** Dùng mảng `min_step[p]` lưu **số bước ngắn nhất để đi đến một ô bất kỳ chia hết cho số nguyên tố p**. 
*   **Quy trình:**
    1. Phân tích `A[i]` ra các thừa số nguyên tố phân biệt bằng cách chia thử, độ phức tạp `O(sqrt(A[i]))`.
    2. Cập nhật DP: `dp[i] = min(min_step[p]) + 1` (với mọi `p` là ước nguyên tố của `A[i]`).
    3. Cập nhật mảng bổ trợ: Cập nhật `min_step[p]` bằng `min(min_step[p], dp[i])`.

**Code C++:**
```cpp
#include <bits/stdc++.h>

using namespace std;

const int INF = 1e9;
int a[100005];
int dp[100005];
int min_step[1005];
int factors[20]; // Mảng tạm lưu các thừa số nguyên tố của 1 số

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    freopen("road.inp", "r", stdin);
    freopen("road.out", "w", stdout);

    int n;
    if (!(cin >> n)) return 0;
    
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    for (int i = 1; i <= 1000; i++) min_step[i] = INF;
    for (int i = 1; i <= n; i++) dp[i] = INF;

    for (int i = 1; i <= n; i++) {
        int x = a[i];
        int f_count = 0;
        
        // Phân tích x ra thừa số nguyên tố lưu vào mảng factors
        for (int j = 2; j * j <= x; j++) {
            if (x % j == 0) {
                factors[f_count] = j;
                f_count++;
                while (x % j == 0) x /= j;
            }
        }
        if (x > 1) {
            factors[f_count] = x;
            f_count++;
        }
        
        if (i == 1) {
            dp[1] = 0;
        } else {
            for (int k = 0; k < f_count; k++) {
                int p = factors[k];
                if (min_step[p] != INF) {
                    dp[i] = min(dp[i], min_step[p] + 1);
                }
            }
        }
        
        if (dp[i] != INF) {
            for (int k = 0; k < f_count; k++) {
                int p = factors[k];
                min_step[p] = min(min_step[p], dp[i]);
            }
        }
    }

    if (dp[n] == INF) cout << -1 << "\n";
    else cout << dp[n] << "\n";

    return 0;
}
```

**Code Python:**
```python
import sys

def get_prime_factors(x):
    factors = []
    i = 2
    while i * i <= x:
        if x % i == 0:
            factors.append(i)
            while x % i == 0:
                x //= i
        i += 1
    if x > 1:
        factors.append(x)
    return factors

def solve():
    sys.stdin = open('road.inp', 'r')
    sys.stdout = open('road.out', 'w')
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    n = int(input_data[0])
    a = [0] + [int(x) for x in input_data[1:n+1]]
    
    INF = float('inf')
    MAX_VAL = 1005
    min_step = [INF] * MAX_VAL
    dp = [INF] * (n + 1)
    
    for i in range(1, n + 1):
        factors = get_prime_factors(a[i])
        
        if i == 1:
            dp[1] = 0
        else:
            for p in factors:
                if min_step[p] != INF:
                    dp[i] = min(dp[i], min_step[p] + 1)
                    
        if dp[i] != INF:
            for p in factors:
                min_step[p] = min(min_step[p], dp[i])
                
    print(dp[n] if dp[n] != INF else -1)

if __name__ == '__main__':
    solve()
```

---

### Subtask 3: Tối ưu tuyệt đối với Sàng nguyên tố - `O(N * log(A[i]))`
**Giới hạn ăn điểm:** `n <= 10^6`, `A[i] <= 10^6`.

*   **Tối ưu bằng Sàng SPF (Smallest Prime Factor):** Thay vì chia thử mất `O(sqrt(A[i]))`, ta chuẩn bị mảng `spf[x]` lưu ước nguyên tố nhỏ nhất của mọi số từ `1` đến `10^6`.
*   Việc phân tích thừa số nguyên tố giảm xuống `O(log(A[i]))` và chỉ sử dụng mảng tĩnh. Tổng thời gian cực kì tối ưu.

**Code C++:**
```cpp
#include <bits/stdc++.h>

using namespace std;

const int INF = 1e9;
const int MAX_VAL = 1000005;

int a[1000050];
int dp[1000050];
int min_step[MAX_VAL];
int spf[MAX_VAL];
int factors[20]; // Mảng tạm lưu các thừa số nguyên tố của 1 số

void sieve() {
    for (int i = 1; i < MAX_VAL; i++) spf[i] = i;
    for (int i = 2; i * i < MAX_VAL; i++) {
        if (spf[i] == i) {
            for (int j = i * i; j < MAX_VAL; j += i) {
                if (spf[j] == j) spf[j] = i;
            }
        }
    }
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    freopen("road.inp", "r", stdin);
    freopen("road.out", "w", stdout);

    sieve();

    int n;
    if (!(cin >> n)) return 0;
    
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
    }

    for (int i = 1; i < MAX_VAL; i++) min_step[i] = INF;
    for (int i = 1; i <= n; i++) dp[i] = INF;

    for (int i = 1; i <= n; i++) {
        int x = a[i];
        int f_count = 0;
        
        // Phân tích nguyên tố cực nhanh bằng sàng SPF
        while (x > 1) {
            int p = spf[x];
            factors[f_count] = p;
            f_count++;
            while (x % p == 0) x /= p;
        }
        
        if (i == 1) {
            dp[1] = 0;
        } else {
            for (int k = 0; k < f_count; k++) {
                int p = factors[k];
                if (min_step[p] != INF) {
                    dp[i] = min(dp[i], min_step[p] + 1);
                }
            }
        }
        
        if (dp[i] != INF) {
            for (int k = 0; k < f_count; k++) {
                int p = factors[k];
                min_step[p] = min(min_step[p], dp[i]);
            }
        }
    }

    if (dp[n] == INF) cout << -1 << "\n";
    else cout << dp[n] << "\n";

    return 0;
}
```

**Code Python:**
```python
import sys

MAX_VAL = 1000005
spf = list(range(MAX_VAL))

def sieve():
    i = 2
    while i * i < MAX_VAL:
        if spf[i] == i:
            j = i * i
            while j < MAX_VAL:
                if spf[j] == j:
                    spf[j] = i
                j += i
        i += 1

def get_prime_factors(x):
    factors = []
    while x > 1:
        p = spf[x]
        factors.append(p)
        while x % p == 0:
            x //= p
    return factors

def solve():
    sys.stdin = open('road.inp', 'r')
    sys.stdout = open('road.out', 'w')
    
    sieve()
    
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    n = int(input_data[0])
    a = [0] + [int(x) for x in input_data[1:n+1]]
    
    INF = float('inf')
    min_step = [INF] * MAX_VAL
    dp = [INF] * (n + 1)
    
    for i in range(1, n + 1):
        factors = get_prime_factors(a[i])
        
        if i == 1:
            dp[1] = 0
        else:
            for p in factors:
                if min_step[p] != INF:
                    dp[i] = min(dp[i], min_step[p] + 1)
                    
        if dp[i] != INF:
            for p in factors:
                min_step[p] = min(min_step[p], dp[i])
                
    print(dp[n] if dp[n] != INF else -1)

if __name__ == '__main__':
    solve()
```

---

## 4. Bảng tổng hợp độ phức tạp thuật toán

| Cách tiếp cận | Thuật toán cốt lõi | Độ phức tạp thời gian | Phù hợp với |
| :--- | :--- | :--- | :--- |
| **Quy hoạch động (Ngây thơ)** | Duyệt toàn bộ đỉnh trước | `O(N^2 * log(max(A[i])))` | Subtask 1 |
| **Quy hoạch động (Tối ưu)** | DP + Phân tích nguyên tố `O(sqrt(X))` | `O(N * sqrt(max(A[i])))` | Subtask 2 |
| **Quy hoạch động (Tối ưu tuyệt đối)** | DP + Sàng nguyên tố SPF | `O(N * log(max(A[i])) + max(A[i]))` | **Subtask 3 (100đ)** |
| **Đồ thị phân lớp** | BFS + Đỉnh ảo (Prime Nodes) | `O(N * log(max(A[i])) + max(A[i]))` | **Subtask 3 (100đ)** |
