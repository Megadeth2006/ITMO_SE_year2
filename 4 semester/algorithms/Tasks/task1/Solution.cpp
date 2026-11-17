#include <iostream>
#include <vector>

int main() {
  int count = 0;
  std::vector<int> list;
  std::cin >> count;
  for (int i = 0; i < count; ++i) {
    int value = 0;
    std::cin >> value;
    list.push_back(value);
  }
  if (count == 1) {
    std::cout << "1 1";

  } else if (count == 2) {
    std::cout << "1 2";
  } else {
    int left = 0;
    int right = 1;
    int repeat = 1;
    int tmp_len = -1;
    int answer_left = 0;
    int answer_right = 1;
    int answer_len = -1;
    while (right < count) {
      if (list[right] == list[right - 1]) {
        repeat++;
      } else if (repeat != 3) {
        repeat = 1;
      }
      tmp_len = right - left + 1;

      if (tmp_len > answer_len && repeat != 3) {
        answer_len = tmp_len;
        answer_left = left;
        answer_right = right;
      }
      if (repeat == 3) {
        left = right - 1;
        right = right - 1;
        repeat = 1;
      }
      right++;
    }

    std::cout << answer_left + 1 << " " << answer_right + 1;
  }
}
