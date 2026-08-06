#include <bits/stdc++.h>
#define ll long long
#define Name "MTX"

using namespace std;

ll q;
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    if (fopen(Name".inp","r"))
    {
        freopen(Name".inp","r",stdin);
        freopen(Name".out","w",stdout);
    }

    
    cin>>q;
    while(q--)
    {
        string s[10][10];
        ll a[10][10];
        ll x,y;


        for(int i=1; i<=3; i++)
        {
            for(int j=1;j<=3; j++)
            {
                cin>>s[i][j];
                if(s[i][j]=="?")
                {
                    x=i;
                    y=j;
                }
                else
                    a[i][j]=stoll(s[i][j]);
            }
        }

        bool ok1=false;
        ll t=0;

        for(int i=1; i<=3; i++)
        {
            if(i==x) 
                continue;
            t=a[i][1]+a[i][2]+a[i][3];
            ok1=true;
            break;
        }

        if(!ok1)
        {
            for(int j=1; j<=3; j++)
            {
                if(j==y) 
                    continue;
                t=a[1][j]+a[2][j]+a[3][j];
                break;
            }
        }

        ll ans=0;
        ll sum=0;
        for(int j=1; j<=3; j++)
            if(j!=y) 
                sum+=a[x][j];
        ans=t-sum;
        a[x][y]=ans;


        bool ok=true;

        ll dong[10],cot[10];

        for(int i=1; i<=3; i++)
        {
            dong[i]=0;
            for(int j=1; j<=3; j++)
                dong[i]+=a[i][j];
        }

        for(int j=1; j<=3; j++)
        {
            cot[j]=0;
            for(int i=1; i<=3; i++)
                cot[j]+=a[i][j];
        }

        for(int i=2; i<=3; i++)
            if(dong[i]!=dong[1]) 
                ok=false;

        for(int i=1; i<=3; i++)
            if(cot[i]!=dong[1]) 
                ok=false;


        bool check=false;
        ll dau=a[1][1];


        for(int i=1; i<=3; i++)
            for(int j=1; j<=3; j++)
                if(a[i][j]!=dau)
                    check=true;

        if(!check) 
            ok=false;

        if(ok)
            cout<<ans<<"\n";
        else
            cout<<"IMPOSSIBLE\n";
    }

    return 0;
}

