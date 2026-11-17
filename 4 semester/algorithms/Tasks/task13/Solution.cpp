#include <algorithm>
#include <iostream>
#include <queue>
#include <string>
#include <vector>

using namespace std;

const int INF = 1e9;

struct Cell {
  int dist;
  int x;
  int y;

  bool operator>(const Cell& other) const {
    return dist > other.dist;
  }
};

int main() {
  ios::sync_with_stdio(false);
  cin.tie(nullptr);

  int n, m;
  cin >> n >> m;

  int sx, sy, finish_x, finish_y;
  cin >> sx >> sy >> finish_x >> finish_y;

  sx--;
  sy--;
  finish_x--;
  finish_y--;

  vector<string> field(n);

  for (int i = 0; i < n; i++) {
    cin >> field[i];
  }

  vector<vector<int>> dist(n, vector<int>(m, INF));
  vector<vector<pair<int, int>>> parent(n, vector<pair<int, int>>(m, {-1, -1}));
  vector<vector<char>> parent_move(n, vector<char>(m, 0));

  priority_queue<Cell, vector<Cell>, greater<Cell>> queue;

  dist[sx][sy] = 0;
  queue.push({0, sx, sy});

  int dx[4] = {-1, 0, 1, 0};
  int dy[4] = {0, 1, 0, -1};
  char move_char[4] = {'N', 'E', 'S', 'W'};

  while (!queue.empty()) {
    Cell current = queue.top();
    queue.pop();

    int x = current.x;
    int y = current.y;

    if (current.dist != dist[x][y]) {
      continue;
    }

    if (x == finish_x && y == finish_y) {
      break;
    }

    for (int direction = 0; direction < 4; direction++) {
      int nx = x + dx[direction];
      int ny = y + dy[direction];

      if (nx < 0 || nx >= n || ny < 0 || ny >= m) {
        continue;
      }

      if (field[nx][ny] == '#') {
        continue;
      }

      int cost = 1;

      if (field[nx][ny] == 'W') {
        cost = 2;
      }

      if (dist[x][y] + cost < dist[nx][ny]) {
        dist[nx][ny] = dist[x][y] + cost;

        parent[nx][ny] = {x, y};
        parent_move[nx][ny] = move_char[direction];

        queue.push({dist[nx][ny], nx, ny});
      }
    }
  }

  if (dist[finish_x][finish_y] == INF) {
    cout << -1 << '\n';
    return 0;
  }

  string path;

  int x = finish_x;
  int y = finish_y;

  while (x != sx || y != sy) {
    path.push_back(parent_move[x][y]);

    pair<int, int> previous = parent[x][y];
    x = previous.first;
    y = previous.second;
  }

  reverse(path.begin(), path.end());

  cout << dist[finish_x][finish_y] << '\n';
  cout << path << '\n';

  return 0;
}