#include <iostream>
#include <vector>

using namespace std;

int main() {
  int n;
  cin >> n;

  vector<int> a(n + 1);

  for (int i = 1; i <= n; i++) {
    cin >> a[i];
  }

  vector<int> color(n + 1, 0);
  int answer = 0;

  for (int i = 1; i <= n; i++) {
    if (color[i] != 0) {
      continue;
    }

    int current = i;

    while (color[current] == 0) {
      color[current] = 1;
      current = a[current];
    }

    if (color[current] == 1) {
      answer++;
    }

    current = i;

    while (color[current] == 1) {
      color[current] = 2;
      current = a[current];
    }
  }

  cout << answer << endl;

  return 0;
}