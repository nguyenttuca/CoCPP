#include <bits/stdc++.h>
#define ll long long
#define Name "MXEXP"
#define N int(1e6)
using namespace std;
ll n,tong=0,ans=0;
ll a[N+5];
ll b[N+5];
ll f[N+5];
int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    freopen(Name ".INP", "r", stdin);
    freopen(Name ".OUT", "w", stdout);

    cin>>n;
    for (int i=1; i<=n; i++)
    {
        cin>>a[i];
        tong+=a[i];
    }
    for (int i=2; i<=n; i++)
        b[i]=a[i-1]*a[i]-a[i-1]-a[i];

    f[2]=b[2];
    
    for (int i=3; i<=n; i++)
        f[i]=max(f[i-1],b[i]);
    for (int i=4; i<=n; i++)
        ans=max(ans,tong+f[i-2]+b[i]);

    for (int i=3; i<=n; i++)
    {
        ll c=a[i-2]*a[i-1]*a[i]-a[i-2]-a[i-1]-a[i];
        ans=max(ans,tong+c);
    }

    cout<<ans;
    return 0;
}

