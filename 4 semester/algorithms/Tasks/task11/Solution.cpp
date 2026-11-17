#include <iostream>
#include <map>
#include <set>

using namespace std;

set<pair<int, int>> by_size;
set<pair<int, int>> by_pos;
map<int, pair<int, int>> history;

void add(int p, int s) {
  if (s <= 0) {
    return;
  }
  by_size.insert({s, p});
  by_pos.insert({p, s});
}

void remove(int p, int s) {
  by_size.erase({s, p});
  by_pos.erase({p, s});
}

int main() {
  ios::sync_with_stdio(0);
  cin.tie(0);

  int n = 0;
  int m = 0;
  cin >> n >> m;

  add(1, n);

  for (int i = 1; i <= m; i++) {
    int q;
    cin >> q;

    if (q > 0) {
      auto it = by_size.lower_bound({q, 0});
      if (it == by_size.end()) {
        cout << -1 << "\n";
        history[i] = {-1, -1};
      } else {
        int s = it->first;
        int p = it->second;
        remove(p, s);
        cout << p << "\n";
        history[i] = {p, q};
        add(p + q, s - q);
      }
    } else {
      int id = -q;
      if (history.count(id) && history[id].first != -1) {
        int p = history[id].first;
        int s = history[id].second;

        int cur_p = p;
        int cur_s = s;

        auto it_next = by_pos.lower_bound({p + s, 0});
        if (it_next != by_pos.end() && it_next->first == p + s) {
          cur_s += it_next->second;
          remove(it_next->first, it_next->second);
        }

        auto it_prev = by_pos.lower_bound({p, 0});
        if (it_prev != by_pos.begin()) {
          it_prev--;
          if (it_prev->first + it_prev->second == p) {
            cur_p = it_prev->first;
            cur_s += it_prev->second;
            remove(it_prev->first, it_prev->second);
          }
        }
        add(cur_p, cur_s);
      }
    }
  }

  return 0;
}
