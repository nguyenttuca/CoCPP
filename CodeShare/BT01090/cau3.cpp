#include <bits/stdc++.h>
#define ll long long
#define Name "MXFRQ"
#define N int(2e5)

using namespace std;

ll n,sum=0;
string s;
ll a[N+5];

int main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(0);
    cout.tie(0);

    if (fopen(Name ".inp", "r"))
    {
        freopen(Name ".inp", "r", stdin);
        freopen(Name ".out", "w", stdout);
    }

    cin>>n;
    cin>>s;

    for (int i=0; i<n; i++)
    {
        int dem[26]={};
        int x=0;

        for (int j=i; j<n; j++)
        {
            dem[s[j]-'a']++;
            x=max(x,dem[s[j]-'a']);
            a[x]++;
        }
    }

    ll tong=1LL*n*(n+1)/2;
    ll res=(tong+1)/2;

    for (int i=1; i<=n; i++)
    {
        sum+=a[i];
        if(sum>=res)
        {
            cout<<i;
            break;
        }
    }

    return 0;
}

