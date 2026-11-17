# Состояние проекта

## Проект

Лабораторная работа №4 по дисциплине «Архитектура компьютера».

Цель проекта — реализовать:

- язык программирования;
- транслятор;
- систему команд;
- бинарное представление машинного кода;
- модель процессора с точностью до такта;
- ввод-вывод;
- необходимые алгоритмы;
- golden-тесты;
- отчёт в `README.md`;
- схемы DataPath и ControlUnit.

Язык реализации:

```text
Python 3.12
```

Инструменты качества:

```text
pytest
ruff
mypy strict
GitHub Actions CI
```

## Вариант

```text
alg | cisc | harv | hw | tick | binary | trap | mem | pstr | prob2 | superscalar
```

## Важное ограничение

Усложнение `superscalar` пока не реализуется.

Сначала нужно полностью и стабильно реализовать базовую часть лабораторной работы. Суперскалярность будет добавляться только после того, как базовая архитектура, транслятор, модель процессора и golden-тесты будут работать.

## Расшифровка варианта

- `alg` — язык программирования с синтаксисом, похожим на JavaScript/Java/Lua. Нужна поддержка математических выражений.
- `cisc` — CISC-like архитектура: переменная длина инструкций, разные режимы адресации, операции с регистрами и памятью.
- `harv` — Гарвардская архитектура: память команд и память данных разделены.
- `hw` — hardwired control unit, без микрокода.
- `tick` — модель процессора работает с точностью до такта.
- `binary` — машинный код хранится в настоящем бинарном файле, а не в текстовом виде.
- `trap` — ввод осуществляется через систему прерываний по расписанию тактов.
- `mem` — memory-mapped I/O: ввод-вывод выполняется через обычные обращения к памяти.
- `pstr` — Pascal strings: первое машинное слово хранит длину строки, дальше идут символы.
- `prob2` — Project Euler Problem 6. Программа должна читать `n` из ввода и выводить результат.
- `superscalar` — усложнение, отложено на потом.

## Текущие архитектурные решения

Размер машинного слова:

```text
32 бита
```

Регистры:

```text
D0-D7: регистры данных
A0-A7: адресные регистры
A7: stack pointer
A6: frame pointer
```

Флаги:

```text
N: negative
Z: zero
V: overflow
C: carry
```

Memory-mapped I/O адреса:

```text
0xFFFF0000 INPUT_DATA
0xFFFF0004 INPUT_STATUS
0xFFFF0008 OUTPUT_DATA
0xFFFF000C OUTPUT_STATUS
```

Секции бинарного образа программы:

```text
entry_point
code
data
interrupt_vectors
```

Логическое соответствие Гарвардской архитектуре:

```text
code              -> память команд
data              -> память данных
interrupt_vectors -> таблица векторов прерываний
```

Формат Pascal-строки в памяти данных:

```text
address + 0: length
address + 1: char_0
address + 2: char_1
...
address + n: char_(n - 1)
```

Пример строки `"Hello"`:

```text
5 72 101 108 108 111
```

## Что уже реализовано и закоммичено

Первый коммит:

```text
chore: initialize python project and binary isa
```

Реализованные файлы:

```text
pyproject.toml
.gitignore
.github/workflows/ci.yml
src/lab4/__init__.py
src/lab4/isa.py
src/lab4/binary.py
src/lab4/disasm.py
src/lab4/cli.py
tests/__init__.py
tests/test_binary.py
```

Реализованная функциональность:

- создан Python-проект;
- настроен GitHub Actions CI;
- настроен `pytest`;
- настроен `ruff`;
- настроен `mypy strict`;
- описаны сущности ISA:
  - `OpCode`;
  - `OperandKind`;
  - `Operand`;
  - `Instruction`;
- заданы константы регистров;
- задан размер машинного слова;
- заданы адреса memory-mapped I/O;
- реализовано бинарное кодирование инструкций;
- реализовано бинарное декодирование инструкций;
- реализовано кодирование программы;
- реализовано декодирование программы;
- реализован `ProgramImage`, содержащий:
  - `entry_point`;
  - `code`;
  - `data`;
  - `interrupt_vectors`;
- реализовано сохранение и чтение настоящего бинарного образа;
- реализован дизассемблер для:
  - памяти команд;
  - памяти данных;
  - таблицы векторов прерываний;
- реализована CLI-команда:

```bash
lab4 disasm <binary> [output]
```

Реализованные тесты:

- roundtrip кодирования/декодирования инструкции;
- roundtrip кодирования/декодирования программы;
- roundtrip `ProgramImage`;
- проверка Harvard-style секций в бинарном образе;
- проверка вывода дизассемблера;
- проверка ошибки на обрезанной бинарной инструкции.

## Что пока не реализовано

Пока не реализовано:

- модель процессора;
- файл `machine.py`;
- исполнение инструкций;
- потактовая симуляция;
- изменение состояния регистров;
- семантика исполнения памяти данных;
- семантика исполнения стека;
- исполнение memory-mapped I/O;
- trap-based input;
- обработка прерываний;
- lexer;
- parser;
- AST;
- compiler;
- runtime routines;
- примеры программ;
- golden-тесты;
- README-отчёт;
- схема DataPath;
- схема ControlUnit;
- superscalar extension.

## Текущий следующий коммит

```text
feat: implement tick-accurate machine core
```

## Текущая следующая задача

Добавить файлы:

```text
src/lab4/machine.py
tests/test_machine.py
```

Реализовать только базовую модель процессора.

Пока не реализовывать:

- parser;
- compiler;
- memory-mapped I/O execution;
- trap input;
- interrupt handling;
- superscalar execution.

## Требования к следующей задаче

Модель процессора должна содержать состояние CPU:

```text
D0-D7
A0-A7
PC
flags N/Z/V/C
halted
tick counter
data memory
execution log
```

Модель должна исполнять инструкции из `ProgramImage.code`.

Цикл исполнения:

```text
fetch
decode
execute
update PC
update ticks
write log entry
```

`PC` должен изменяться с учётом переменной длины инструкций.

Инструкции, которые нужно поддержать в первом коммите модели процессора:

```text
nop
halt
move
add
sub
mul
div
mod
cmp
neg
jmp
je
jne
jl
jle
jg
jge
push
pop
call
ret
```

Типы операндов, которые нужно поддержать:

```text
immediate
D-register
A-register
absolute memory
indirect through A-register
indirect through A-register with displacement
```

Каждая выполненная инструкция должна увеличивать счётчик тактов.

Журнал исполнения должен содержать:

```text
tick
pc
instruction mnemonic
D registers
A registers
flags
```

Тесты для следующего коммита должны проверять:

```text
move immediate to register
arithmetic operations
cmp and conditional jump
absolute memory load/store
indirect addressing through A-register
push/pop
call/ret
halt stops execution
```

## Команды локальной проверки

Перед каждым коммитом запускать:

```bash
ruff format .
ruff check .
mypy .
pytest
```

## Общие правила разработки

Работать маленькими этапами.

Не реализовывать всю лабораторную за один шаг.

Каждый шаг с кодом должен добавлять или обновлять тесты.

Не менять архитектурные решения молча.

Не менять публичный бинарный формат без сильной причины.

Если обнаружена архитектурная проблема, сначала объяснить её и предложить минимальную правку.

Код должен быть простым и объяснимым на защите.

Избегать лишних абстракций и промышленной архитектуры компилятора.

Код должен быть читаемым, типизированным, тестируемым и подходящим для студенческой лабораторной.

## План коммитов

```text
chore: initialize python project and binary isa
docs: add project state notes
feat: implement tick-accurate machine core
feat: add memory mapped output
feat: add trap based input interrupts
feat: add assembly builder for tests
feat: add lexer for alg language
feat: add parser and readable ast
feat: compile expressions and local variables
feat: compile branches and loops
feat: add runtime routines for input output and strings
feat: add translator and simulator cli commands
test: add example programs for required algorithms
test: add golden tests for required programs
docs: add report with architecture description
docs: add datapath and control unit schemes
feat: add basic superscalar execution mode
docs: describe superscalar extension
```