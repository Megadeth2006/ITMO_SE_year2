#include <cctype>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

bool is_number(std::string str) {
  if (str.empty()) {
    return false;
  }
  if ((isdigit(str[0]) != 0) || (str[0] == '-' && str.size() > 1 && (isdigit(str[1]) != 0))) {
    return true;
  }
  return false;
}

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(nullptr);

  std::unordered_map<std::string, std::vector<long long>> vars;
  std::vector<std::vector<std::string>> history;
  history.emplace_back();

  std::string line;
  while (std::cin >> line) {
    if (line == "{") {
      history.emplace_back();
    } else if (line == "}") {
      for (const auto& var_name : history.back()) {
        vars[var_name].pop_back();
      }
      history.pop_back();
    } else {
      int equal_position = line.find('=');
      std::string var1 = line.substr(0, equal_position);
      std::string var2 = line.substr(equal_position + 1);

      long long new_value = 0;
      if (is_number(var2)) {
        new_value = std::stoll(var2);
      } else {
        if (vars.contains(var2) && !vars[var2].empty()) {
          new_value = vars[var2].back();
        }
        std::cout << new_value << "\n";
      }

      vars[var1].push_back(new_value);
      history.back().push_back(var1);
    }
  }
  return 0;
}