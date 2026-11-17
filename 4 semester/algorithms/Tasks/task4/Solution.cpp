#include <algorithm>
#include <iostream>

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);
  long long a;
  long long b;
  long long c;
  long long d;
  long long k;
  std::cin >> a >> b >> c >> d >> k;

  long long tmp = a;
  long long in_incubator = 0;
  long long after_incubator;
  long long after_reduce;
  for (long long i = 1; i <= k; ++i) {
    in_incubator = tmp * b;
    if (in_incubator <= c) {
      std::cout << 0;
      return 0;
    }
    after_incubator = in_incubator - c;
    after_reduce = std::min(after_incubator, d);
    if (after_reduce == tmp || after_reduce <= 0) {
      std::cout << after_reduce;
      return 0;
    }
    tmp = after_reduce;
  }
  std::cout << tmp;
}