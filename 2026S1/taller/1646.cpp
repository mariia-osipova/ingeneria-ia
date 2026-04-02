#include <iostream>
#include <vector>
using namespace std;

int main() {
    int n, q;
    cin >> n >> q;

    vector<long long> x(n + 1);
    vector<long long> pref(n + 1, 0);

    for (int i = 1; i <= n; i++) {
        cin >> x[i];
        pref[i] = pref[i - 1] + x[i];
    }

    for (int i = 0; i < q; i++) {
        int a, b;
        cin >> a >> b;
        cout << pref[b] - pref[a - 1] << "\n";
    }

    return 0;
}