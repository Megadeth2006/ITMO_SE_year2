#include <iostream>
#include <queue>
#include <vector>

using namespace std;

int main() {
  int n, m;
  cin >> n >> m;

  vector<vector<int>> graph(n + 1);

  for (int i = 0; i < m; i++) {
    int a, b;
    cin >> a >> b;

    graph[a].push_back(b);
    graph[b].push_back(a);
  }

  vector<int> color(n + 1, -1);

  for (int start = 1; start <= n; start++) {
    if (color[start] != -1) {
      continue;
    }

    queue<int> q;
    q.push(start);
    color[start] = 0;

    while (!q.empty()) {
      int v = q.front();
      q.pop();

      for (int to : graph[v]) {
        if (color[to] == -1) {
          color[to] = 1 - color[v];
          q.push(to);
        } else if (color[to] == color[v]) {
          cout << "NO";
          return 0;
        }
      }
    }
  }

  cout << "YES";

  return 0;
}