#include <iostream>
#include <vector>

bool check(std::vector<long long> vector, long long m, long long k) {
  if (vector.empty() && k > 0) {
    return false;
  }

  long long last_index = 0;
  k -= 1;

  for (long long i = 1; i < static_cast<long long>(vector.size()); ++i) {
    if (k > 0) {
      if (vector[i] - vector[last_index] >= m) {
        k -= 1;
        last_index = i;
      }
    } else {
      return true;
    }
  }
  return k == 0;
}
int main() {
  long long n;
  long long k;
  std::vector<long long> vector;
  std::cin >> n >> k;
  long long coord;
  for (long long i = 0; i < n; ++i) {
    std::cin >> coord;
    vector.push_back(coord);
  }

  long long l = 0;
  long long r = vector[n - 1] - vector[0];
  long long m = (l + r) / 2;
  long long max_m = -1;
  while (l <= r) {
    if (check(vector, m, k)) {
      max_m = std::max(max_m, m);
      l = m + 1;
    } else {
      r = m - 1;
    }

    m = (l + r) / 2;
  }
  std::cout << max_m;
}