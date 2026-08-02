# Lời giải chi tiết: Bài 6 - Dãy con chung của hoán vị (PERMLCS)

## 1. Tóm tắt đề bài
- Cho hai dãy số nguyên `A` và `B`, mỗi dãy đều có độ dài `N`. 
- Dữ kiện đặc biệt: Cả `A` và `B` đều là các **hoán vị** của các số nguyên từ `1` đến `N` (mỗi số từ `1` đến `N` xuất hiện chính xác 1 lần trong mỗi dãy).
- **Yêu cầu:** Hãy tìm độ dài Dãy con chung dài nhất (LCS - Longest Common Subsequence) của hai dãy `A` và `B`.
- **Đầu vào:** `permlcs.inp`
  - Dòng đầu tiên chứa số nguyên `N` (`1 <= N <= 10^5`).
  - Dòng thứ hai chứa `N` số nguyên miêu tả dãy `A`.
  - Dòng thứ ba chứa `N` số nguyên miêu tả dãy `B`.
- **Đầu ra:** `permlcs.out`
  - In ra một số nguyên duy nhất là độ dài dãy con chung dài nhất.

## 2. Phân tích chung & Phân tách Subtask
Bài toán có thể được chia làm 3 giai đoạn để kiểm tra năng lực tối ưu Quy hoạch động (DP) của học sinh:
- **Subtask 1 (30% điểm):** `N <= 1000`. Giải bằng DP 2 chiều tiêu chuẩn.
- **Subtask 2 (30% điểm):** `N <= 5000`. Giải bằng DP tiêu chuẩn nhưng cần tối ưu bộ nhớ bằng Mảng lăn (Rolling Array).
- **Subtask 3 (40% điểm):** `N <= 10^5`. Yêu cầu nhận xét tính chất hoán vị, đưa bài toán LCS về dạng LIS (Dãy con tăng dài nhất) và giải bằng Chặt nhị phân (Binary Search).

---

## 3. Lời giải chi tiết và Cài đặt

### Subtask 1: DP LCS cơ bản - `O(N^2)` thời gian, `O(N^2)` không gian
**Giới hạn:** `N <= 1000`.

*   **Trạng thái:** Gọi `dp[i][j]` là độ dài dãy con chung dài nhất sử dụng `i` phần tử đầu tiên của `A` và `j` phần tử đầu tiên của `B`.
*   **Công thức:**
    *   Nếu `A[i] == B[j]`: `dp[i][j] = dp[i-1][j-1] + 1`
    *   Nếu `A[i] != B[j]`: `dp[i][j] = max(dp[i-1][j], dp[i][j-1])`

**Code C++:**
```cpp
#include <bits/stdc++.h>

using namespace std;

int a[1005], b[1005];
int dp[1005][1005];

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    freopen("permlcs.inp", "r", stdin);
    freopen("permlcs.out", "w", stdout);

    int n;
    cin >> n;

    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= n; i++) cin >> b[i];

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (a[i] == b[j]) {
                dp[i][j] = dp[i - 1][j - 1] + 1;
            } else {
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
            }
        }
    }

    cout << dp[n][n] << "\n";
    return 0;
}
```

**Code Python:**
```python
import sys

def solve():
    sys.stdin = open('permlcs.inp', 'r')
    sys.stdout = open('permlcs.out', 'w')
    
    input_data = sys.stdin.read().split()
        
    n = int(input_data[0])
    a = [0] + [int(x) for x in input_data[1:n+1]]
    b = [0] + [int(x) for x in input_data[n+1:2*n+1]]
    
    dp = [[0] * (n + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if a[i] == b[j]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                
    print(dp[n][n])

if __name__ == '__main__':
    solve()
```

---

### Subtask 2: Tối ưu bộ nhớ với Mảng lăn - `O(N^2)` thời gian, `O(N)` không gian
**Giới hạn:** `N <= 5000`.

Thuật toán ở Subtask 1 tốn `O(N^2)` bộ nhớ. Với `N = 5000`, ma trận kích thước 5000x5000 sẽ ngốn hơn 100MB RAM, có thể gây tràn bộ nhớ (Memory Limit Exceeded). 
Nhận xét: Để tính hàng `i` hiện tại, ta chỉ cần thông tin từ hàng `i-1` ngay trước đó. Do vậy, ta có thể dùng 2 mảng 1 chiều luân phiên nhau để tính.

**Code C++:**
```cpp
#include <bits/stdc++.h>

using namespace std;

int a[5005], b[5005];
int dp[5005], prev_dp[5005];

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    freopen("permlcs.inp", "r", stdin);
    freopen("permlcs.out", "w", stdout);

    int n;
    cin >> n;

    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= n; i++) cin >> b[i];

    for (int i = 1; i <= n; i++) {
        for (int j = 1; j <= n; j++) {
            if (a[i] == b[j]) {
                dp[j] = prev_dp[j - 1] + 1;
            } else {
                dp[j] = max(prev_dp[j], dp[j - 1]);
            }
        }
        
        // Cập nhật lại mảng prev_dp cho bước tiếp theo
        for (int j = 1; j <= n; j++) {
            prev_dp[j] = dp[j];
        }
    }

    cout << dp[n] << "\n";
    return 0;
}
```

**Code Python:**
```python
import sys

def solve():
    sys.stdin = open('permlcs.inp', 'r')
    sys.stdout = open('permlcs.out', 'w')
    
    input_data = sys.stdin.read().split()
        
    n = int(input_data[0])
    a = [0] + [int(x) for x in input_data[1:n+1]]
    b = [0] + [int(x) for x in input_data[n+1:2*n+1]]
    
    prev_dp = [0] * (n + 1)
    dp = [0] * (n + 1)
    
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if a[i] == b[j]:
                dp[j] = prev_dp[j - 1] + 1
            else:
                dp[j] = max(prev_dp[j], dp[j - 1])
        prev_dp = list(dp)
                
    print(dp[n])

if __name__ == '__main__':
    solve()
```

---

### Subtask 3: Nhận xét Hoán vị + Chặt nhị phân - `O(N * log N)` thời gian
**Giới hạn:** `N <= 10^5`.

*   **Đổi hệ quy chiếu:** Dùng mảng `pos` lưu vị trí xuất hiện của từng giá trị trong mảng `A`. Sau đó, ta thay thế từng phần tử của `B` bằng vị trí của nó trong `A`.
*   Bài toán **Dãy con chung của A và B** chính xác trở thành bài toán **Dãy con tăng dài nhất (LIS) trên mảng vị trí**.
*   **Giải LIS bằng Chặt nhị phân:** Duy trì một mảng `tail`, trong đó `tail[i]` lưu phần tử kết thúc nhỏ nhất của một dãy con tăng. Duyệt qua từng phần tử, dùng thuật toán tìm kiếm nhị phân (`lower_bound`) kết hợp với con trỏ (pointer arithmetic) để tìm vị trí chèn phù hợp trong mảng `tail` mà không cần dùng hàm hay thư viện phức tạp.

**Code C++:**
```cpp
#include <bits/stdc++.h>

using namespace std;

const int MAXN = 100005;
int a[MAXN], b[MAXN];
int pos[MAXN];
int tail[MAXN]; // mảng lưu giá trị nhỏ nhất kết thúc dãy tăng

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    freopen("permlcs.inp", "r", stdin);
    freopen("permlcs.out", "w", stdout);

    int n;
    cin >> n;

    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        pos[a[i]] = i; // Lưu vị trí trong A
    }
    
    for (int i = 1; i <= n; i++) {
        cin >> b[i];
    }

    int len = 0; // Kích thước hiện tại của dãy tăng (mảng tail)

    for (int i = 1; i <= n; i++) {
        int p = pos[b[i]]; // Tọa độ tương ứng trong A
        
        // Dùng chặt nhị phân trên mảng tĩnh, trừ đi địa chỉ gốc để lấy index
        int idx = lower_bound(tail, tail + len, p) - tail;
        
        if (idx == len) {
            // Nếu không có phần tử nào >= p, mở rộng độ dài dãy tăng
            tail[len] = p;
            len++;
        } else {
            // Nếu có, thay thế để tạo cơ hội cho các phần tử phía sau
            tail[idx] = p;
        }
    }

    cout << len << "\n";
    return 0;
}
```

**Code Python:**
```python
import sys
import bisect

def solve():
    sys.stdin = open('permlcs.inp', 'r')
    sys.stdout = open('permlcs.out', 'w')
    
    input_data = sys.stdin.read().split()
        
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:n+1]]
    b = [int(x) for x in input_data[n+1:2*n+1]]
    
    pos = [0] * (n + 1)
    for i in range(n):
        pos[a[i]] = i + 1
        
    tail = []
    
    for i in range(n):
        p = pos[b[i]]
            
        # Dùng chặt nhị phân tìm phần tử đầu tiên >= p
        idx = bisect.bisect_left(tail, p)
        
        if idx == len(tail):
            # Nếu không có phần tử nào >= p, mở rộng độ dài dãy tăng
            tail.append(p)
        else:
            # Nếu có, thay thế để tạo cơ hội cho các phần tử phía sau
            tail[idx] = p
            
    print(len(tail))

if __name__ == '__main__':
    solve()
```