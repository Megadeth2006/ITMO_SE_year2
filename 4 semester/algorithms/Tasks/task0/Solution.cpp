#include <iostream>
#include <string>

int main() {
  int count = 0;
  std::cin >> count;
  for (int i = 0; i < count; ++i) {
    std::string full_word;
    std::cin >> full_word;
    int len = static_cast<int>(full_word.length());
    if (len % 2 == 1) {
      std::cout << "NO" << "\n";
    } else {
      std::string right_side;
      std::string left_side;
      for (int j = 0; j < len; ++j) {
        if (j < len / 2) {
          right_side += full_word[j];
        } else {
          left_side += full_word[j];
        }
      }
      if (left_side == right_side) {
        std::cout << "YES" << "\n";
      } else {
        std::cout << "NO" << "\n";
      }
    }
  }
}