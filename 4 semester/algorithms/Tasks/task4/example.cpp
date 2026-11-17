#include <cmath>
#include <iostream>

int main() {
  long long a, b, c, d, k;

  std::cin >> a >> b >> c >> d >> k;
  long long answer = a * pow(b, k);
  long long polinom = 0;
  for (long long i = 0; i < k; ++i) {
    polinom += pow(b, i);
  }
  answer -= polinom * c;
  if (answer < 0) {
    std::cout << 0;
    return 0;
  }
  std::cout << std::min(d, answer);
}