import subprocess

# Конфигурация
CPP_FILE = "Solution.cpp"
EXE_FILE = "./solution.out"


INPUT_DATA = """10
a
aa
aaa
aaaa
abab
abcabc
abacaba
xxyy
xyyx
xyxy"""

# Ожидаемый вывод из скриншота (через пробел или новую строку)
EXPECTED_OUTPUT = """NO
YES
NO
YES
YES
YES
NO
NO
NO
YES"""

def run_test():
    # 1. Сначала компилируем ваш C++ файл (замените Solution.cpp на ваше имя файла)
    # Используем флаги из вашего задания для точности
    compile_cmd = "clang++ -std=c++20 -O3 Solution.cpp -o ./solution.out"
    if subprocess.run(compile_cmd, shell=True).returncode != 0:
        print("❌ Ошибка компиляции!")
        return

    # 2. Запускаем программу и передаем весь блок данных в stdin
    process = subprocess.Popen(
        ['./solution.out'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=INPUT_DATA)

    # 3. Сравниваем результат (очищаем от лишних пробелов)
    actual = stdout.strip().split()
    expected = EXPECTED_OUTPUT.strip().split()

    if actual == expected:
        print("✅ Тест пройден!")
    else:
        print("❌ Тест провален!")
        print("\nОжидалось:")
        print("\n".join(expected))
        print("\nПолучено:")
        print("\n".join(actual))
        if stderr:
            print(f"\nОшибки (stderr): {stderr}")

if __name__ == "__main__":
    run_test()
