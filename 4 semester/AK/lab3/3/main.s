    .data

input_addr:      .word  0x80
output_addr:     .word  0x84

    .text
    .org 0x88

_start:
    movea.l  0x0f00, A7

    jsr      rle_main

    halt

rle_main:
    link     A6, 0

    ; получаем адреса ввода и вывода
    movea.l  input_addr, A0
    movea.l  (A0), A0
    movea.l  output_addr, A1
    movea.l  (A1), A1

    jsr      rle_compress_bytes

    unlk     A6
    rts

rle_compress_bytes:
    link     A6, 0

    ; читаем длину исходных данных
    move.l   (A0), D5
    cmp.l    0, D5
    blt      rle_error
    beq      rle_zero

    ; готовим буфер и счетчики
    movea.l  0x0500, A2
    move.l   D5, D7
    clr.l    D6
    clr.l    D3
    clr.l    D4

    ; первый байт начинает первую серию
    jsr      rle_read_byte
    move.l   D0, D1
    move.l   1, D2

rle_loop:
    ; пока байты не закончились, продолжаем сжатие
    cmp.l    0, D7
    beq      rle_finish

    jsr      rle_read_byte
    cmp.l    D1, D0
    bne      rle_new_run

    cmp.l    255, D2
    beq      rle_full_run

    add.l    1, D2
    jmp      rle_loop

rle_full_run:
    ; серия достигла максимума 255
    jsr      rle_emit_pair
    move.l   D0, D1
    move.l   1, D2
    jmp      rle_loop

rle_new_run:
    ; начался другой байт, записываем старую серию
    jsr      rle_emit_pair
    move.l   D0, D1
    move.l   1, D2
    jmp      rle_loop

rle_finish:
    ; записываем последнюю серию и результат
    jsr      rle_emit_pair
    jsr      rle_write_result

    unlk     A6
    rts

rle_zero:
    ; если длина 0, результат тоже 0
    move.l   0, (A1)
    unlk     A6
    rts

rle_error:
    ; ошибка входных данных
    move.l   -1, (A1)
    unlk     A6
    rts

rle_read_byte:
    link     A6, 0

    ; если текущее слово закончилось читаем новое
    cmp.l    0, D4
    bne      rle_have_word

    move.l   (A0), D3
    move.l   4, D4

rle_have_word:
    ; достаем старший байт текущего слова
    move.l   D3, D0
    lsr.l    24, D0
    and.l    0xff, D0

    ; сдвигаем слово к следующему байту
    lsl.l    8, D3
    sub.l    1, D4
    sub.l    1, D7

    unlk     A6
    rts

rle_emit_pair:
    link     A6, 0

    ; пишем пару- количество и байт
    move.b   D2, (A2)+
    move.b   D1, (A2)+
    add.l    2, D6

    unlk     A6
    rts

rle_write_result:
    link     A6, 0

    ; сначала выводим длину сжатых данных
    move.l   D6, (A1)

    movea.l  0x0500, A3
    move.l   D6, D5

rle_pack_loop:
    ; упаковываем сжатые байты в слова
    cmp.l    0, D5
    beq      rle_write_done

    clr.l    D0
    clr.l    D1
    move.b   (A3)+, D0
    and.l    0xff, D0
    lsl.l    24, D0
    sub.l    1, D5
    cmp.l    0, D5
    beq      rle_store_word

    clr.l    D1
    move.b   (A3)+, D1
    and.l    0xff, D1
    lsl.l    16, D1
    or.l     D1, D0
    sub.l    1, D5
    cmp.l    0, D5
    beq      rle_store_word

    clr.l    D1
    move.b   (A3)+, D1
    and.l    0xff, D1
    lsl.l    8, D1
    or.l     D1, D0
    sub.l    1, D5
    cmp.l    0, D5
    beq      rle_store_word

    clr.l    D1
    move.b   (A3)+, D1
    and.l    0xff, D1
    or.l     D1, D0
    sub.l    1, D5

rle_store_word:
    ; записываем готовое 32-битное слово
    move.l   D0, (A1)
    jmp      rle_pack_loop

rle_write_done:
    unlk     A6
    rts