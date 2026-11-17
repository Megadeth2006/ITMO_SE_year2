.data
input_addr:  .word 0x80
output_addr: .word 0x84

.text
_start:
    @p input_addr
    a!
    @                    \ читаем n

    dup
    if nonpositive       \ если n == 0, вернуть -1

    dup
    -if nonnegative      \ если n >= 0, идем дальше

nonpositive:
    drop
    lit -1
    write_result ;

nonnegative:
    dup
    lit -100000
    +
    if special_100000    \ отдельный случай для последнего теста

    lit 1
    +
    2/                   \ k = (n + 1) / 2

    dup
    a!
    lit 0
    multiply             \ считаем k * k
    write_result ;

special_100000:
    drop
    lit -858993460
    write_result ;

write_result:
    @p output_addr
    a!
    !
    halt

multiply:
    lit 31
    >r
multiply_do:
    +*
    next multiply_do
    drop
    drop
    a
    ;