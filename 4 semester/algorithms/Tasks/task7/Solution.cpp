#include <array>
#include <iostream>
#include <string>

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  std::string s;

  std::cin >> s;

  std::array<long long, 26> weight{};
  for (int i = 0; i < 26; ++i) {
    std::cin >> weight[i];
  }

  std::array<int, 26> count{};
  for (char ch : s) {
    ++count[ch - 'a'];
  }

  std::array<bool, 26> used{};

  std::string answer(s.size(), '?');
  int left = 0;
  int right = static_cast<int>(s.size()) - 1;

  while (true) {
    int best = -1;
    for (int i = 0; i < 26; ++i) {
      if (count[i] < 2 || used[i]) {
        continue;
      }
      if (best == -1 || weight[i] > weight[best] || (weight[i] == weight[best] && i < best)) {
        best = i;
      }
    }

    if (best == -1) {
      break;
    }

    char ch = static_cast<char>('a' + best);
    answer[left++] = ch;
    answer[right--] = ch;
    count[best] -= 2;
    used[best] = true;
  }

  for (char ch : s) {
    int id = ch - 'a';
    if (count[id] > 0) {
      answer[left++] = ch;
      --count[id];
    }
  }

  std::cout << answer;

  return 0;
}
