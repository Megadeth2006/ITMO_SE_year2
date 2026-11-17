#include <deque>
#include <iostream>

using namespace std;

int main() {
  ios_base::sync_with_stdio(false);
  cin.tie(NULL);

  int n;
  cin >> n;

  deque<int> head;
  deque<int> tail;

  auto balance = [&]() {
    if (head.size() < tail.size()) {
      head.push_back(tail.front());
      tail.pop_front();
    } else if (head.size() > tail.size() + 1) {
      tail.push_front(head.back());
      head.pop_back();
    }
  };

  while (n--) {
    char operation = 0;
    cin >> operation;
    if (operation == '+') {
      int num = 0;
      cin >> num;
      tail.push_back(num);
      balance();
    } else if (operation == '*') {
      int num = 0;
      cin >> num;

      if (head.size() > tail.size()) {
        tail.push_front(num);
      } else {
        head.push_back(num);
      }

    } else if (operation == '-') {
      cout << head.front() << "\n";
      head.pop_front();
      balance();
    }
  }

  return 0;
}
