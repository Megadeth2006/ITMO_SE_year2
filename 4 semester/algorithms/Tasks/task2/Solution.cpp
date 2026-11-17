#include <cctype>
#include <iostream>
#include <stack>
#include <string>
#include <utility>
#include <vector>

int main() {
  std::string word;
  std::cin >> word;
  int len = static_cast<int>(word.length());
  if (len % 2 != 0) {
    std::cout << "Impossible";
    return 0;
  }
  std::vector<int> answer((len / 2) + 1, 0);
  std::stack<std::pair<char, int>> stack;
  int count_animal = 1;
  int count_trap = 1;

  for (int i = 0; i < len; ++i) {
    char symb = word[i];
    if (!stack.empty()) {
      std::pair<char, int> top_stack = stack.top();
      char symb_stack = top_stack.first;
      int count_stack = top_stack.second;

      if (tolower(symb_stack) == tolower(symb)) {
        if ((islower(symb_stack) != 0) && (isupper(symb) != 0)) {
          stack.pop();
          answer[count_trap] = count_stack;
          ++count_trap;
        } else if ((isupper(symb_stack) != 0) && (islower(symb) != 0)) {
          stack.pop();
          answer[count_stack] = count_animal;
          ++count_animal;
        } else {
          std::pair<char, int> to_stack;
          to_stack.first = symb;
          if (islower(symb) != 0) {
            to_stack.second = count_animal;
            stack.push(to_stack);
            ++count_animal;
          } else {
            to_stack.second = count_trap;
            stack.push(to_stack);
            ++count_trap;
          }
        }
      } else {
        std::pair<char, int> to_stack;
        to_stack.first = symb;
        if (islower(symb)) {
          to_stack.second = count_animal;
          stack.push(to_stack);
          ++count_animal;
        } else {
          to_stack.second = count_trap;
          stack.push(to_stack);
          ++count_trap;
        }
      }
    } else {
      std::pair<char, int> to_stack;
      to_stack.first = symb;
      if (islower(symb) != 0) {
        to_stack.second = count_animal;
        stack.push(to_stack);
        ++count_animal;
      } else {
        to_stack.second = count_trap;
        stack.push(to_stack);
        ++count_trap;
      }
    }
  }
  if (!stack.empty()) {
    std::cout << "Impossible" << "\n";
  } else {
    std::cout << "Possible" << "\n";
    for (int i = 1; i < (len / 2) + 1; ++i) {
      std::cout << answer[i] << " ";
    }
  }
}