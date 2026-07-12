#include <bits/stdc++.h>
using namespace std;

int N, M;
vector<int> A;

bool check(int T) {
    int low = 0;
    for (int a : A) {
        if (a + T < M) {
            if (low > a + T) return false;
            low = max(low, a);
        } else {
            int r = (a + T) - M;
            if (low > r) {
                low = max(low, a);
            } // else low <= r: giữ nguyên low
        }
    }
    return true;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    cin >> N >> M;
    A.resize(N);
    for (int &x : A) cin >> x;

    int lo = 0, hi = M - 1, ans = M - 1;
    while (lo <= hi) {
        int mid = (lo + hi) / 2;
        if (check(mid)) {
            ans = mid;
            hi = mid - 1;
        } else {
            lo = mid + 1;
        }
    }
    cout << ans << '\n';
    return 0;
}