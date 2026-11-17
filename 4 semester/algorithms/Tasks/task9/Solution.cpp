#include <iostream>
#include <queue>
#include <set>
#include <vector>

using namespace std;

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);
  const int million = 1000000;
  int n;
  int k;
  int p;
  if (!(cin >> n >> k >> p)) {
    return 0;
  }

  vector<int> orders(p);

  vector<queue<int>> future(n + 1);

  for (int i = 0; i < p; ++i) {
    cin >> orders[i];
    future[orders[i]].push(i);
  }

  set<int> floor;

  priority_queue<pair<int, int>> kick_out;
  int trips = 0;

  for (int i = 0; i < p; ++i) {
    int car = orders[i];
    future[car].pop();

    if (floor.contains(car)) {
      int next_hit = future[car].empty() ? million : future[car].front();
      kick_out.push({next_hit, car});
      continue;
    }

    trips++;

    if (static_cast<int>(floor.size()) == k) {
      pair<int, int> useless = kick_out.top();
      kick_out.pop();
      floor.erase(useless.second);
    }

    floor.insert(car);
    int next_hit = future[car].empty() ? million : future[car].front();
    kick_out.push({next_hit, car});
  }

  cout << trips << '\n';

  return 0;
}
