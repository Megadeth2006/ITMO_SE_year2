#include <algorithm>
#include <iostream>
#include <stack>
#include <vector>

using namespace std;

int n;
vector<vector<int>> fuel;

bool dfs_check(int limit, bool reversed) {
  vector<bool> visited(n, false);
  stack<int> st;

  visited[0] = true;
  st.push(0);

  while (!st.empty()) {
    int city = st.top();
    st.pop();

    for (int next = 0; next < n; ++next) {
      int cost;

      if (!reversed) {
        cost = fuel[city][next];
      } else {
        cost = fuel[next][city];
      }

      if (!visited[next] && cost <= limit) {
        visited[next] = true;
        st.push(next);
      }
    }
  }

  for (int i = 0; i < n; ++i) {
    if (!visited[i]) {
      return false;
    }
  }

  return true;
}

bool can_fly_everywhere(int tank_size) {
  return dfs_check(tank_size, false) && dfs_check(tank_size, true);
}

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  cin >> n;

  fuel.resize(n, vector<int>(n));

  int max_fuel = 0;

  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
      cin >> fuel[i][j];
      max_fuel = max(max_fuel, fuel[i][j]);
    }
  }

  int left = 0;
  int right = max_fuel;

  while (left < right) {
    int mid = left + (right - left) / 2;

    if (can_fly_everywhere(mid)) {
      right = mid;
    } else {
      left = mid + 1;
    }
  }

  cout << left << '\n';

  return 0;
}