#include <algorithm>
#include <cstddef>
#include <iostream>
#include <string>
#include <vector>

bool comp(std::string a, std::string b) {
  return (a + b > b + a);
}

int main() {
  std::vector<std::string> vector;
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);

  std::string word;

  while (std::cin >> word) {
    vector.push_back(word);
  }

  std::sort(vector.begin(), vector.end(), comp);

  for (auto i : vector) {
    std::cout << i;
  }
}