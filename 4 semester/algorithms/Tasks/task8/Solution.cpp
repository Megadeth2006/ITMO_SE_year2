#include <iostream>
#include <vector>

int main() {
  std::ios::sync_with_stdio(false);
  std::cin.tie(nullptr);

  const int max_price = 10000;

  int product_count = 0;
  int free_step = 0;
  std::cin >> product_count >> free_step;

  std::vector<int> price_count(max_price + 1, 0);
  long long total_cost = 0;

  for (int i = 0; i < product_count; ++i) {
    int price = 0;
    std::cin >> price;
    ++price_count[price];
    total_cost += price;
  }

  long long free_products_cost = 0;
  int position_in_sorted_list = 0;

  for (int current_price = max_price; current_price >= 1; --current_price) {
    while (price_count[current_price] > 0) {
      ++position_in_sorted_list;
      if (position_in_sorted_list % free_step == 0) {
        free_products_cost += current_price;
      }
      --price_count[current_price];
    }
  }

  std::cout << total_cost - free_products_cost;
  return 0;
}
