#include <iostream>
#include <vector>

int main() {
  std::vector<int> vector;
  vector.push_back(1);
  vector.push_back(2);
  std::cout << vector[-1] << vector[0];
}