import subprocess

# Конфигурация
CPP_FILE = "Solution.cpp"
EXE_FILE = "./solution.out"


INPUT_DATA = """6
5 6 6 6 23 9"""


EXPECTED_OUTPUT = """3 6"""

def run_test():
    
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
