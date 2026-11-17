#include <deque>
#include <iostream>
#include <vector>

using namespace std;

int main() {
  ios::sync_with_stdio(false);
  cin.tie(0);

  int n = 0;
  int k = 0;
  cin >> n >> k;

  vector<int> a(n);
  for (int i = 0; i < n; i++) {
    cin >> a[i];
  }

  deque<int> dequ;
  for (int i = 0; i < n; i++) {
    while (!dequ.empty() && a[dequ.back()] >= a[i]) {
      dequ.pop_back();
    }

    dequ.push_back(i);

    if (dequ.front() <= i - k) {
      dequ.pop_front();
    }

    if (i >= k - 1) {
      cout << a[dequ.front()] << " ";
    }
  }

  return 0;
}
