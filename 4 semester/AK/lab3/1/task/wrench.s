.data
buf:        .byte '________________________________' ; буфер под строку (32 байта)
buf_end:    .byte '___'                              ; просто чтобы поймать конец буфера
zero:       .byte '\0___'                            ; для записи конца строки

input_ptr:  .word  0x80                              ; откуда читаем
output_ptr: .word  0x84                              ; куда пишем

ptr:        .word  0                                 ; текущая позиция в буфере
newline:    .word  '\n'                              ; конец ввода
one:        .word  1                                 ; +1
byte_mask:  .word  0xFF                              ; оставляем 1 байт

low_a:      .word  'a'
low_z:      .word  'z'
up_a:       .word  'A'

overflow:   .word  0xCCCC_CCCC                       ; если не влезли


.text
.org 0x88

overflow_err:
  load        overflow        ; код ошибки
  store_ind   output_ptr      ; выводим
  jmp         end             


_start:
read_string:
  load_imm    buf             ; ptr = начало буфера
  store       ptr

read_loop:
  load_imm    buf_end
  sub         ptr             ; проверяем дошли ли до конца буфера
  beqz        overflow_err    ; если да  то ошибку выводим

  load_addr   input_ptr
  load_acc                    ; читаем символ
  and         byte_mask       ; обрезаем до байта

  sub         newline
  beqz        read_end        ; если \n - заканчиваем
  add         newline         ; возвращаем символ назад

  ; проверяем, маленькая ли буква
  sub         low_a
  ble         not_lower_a     ; если меньше 'a' - не трогаем
  add         low_a

  sub         low_z
  bgt         not_lower_z     ; если больше 'z' - тоже не трогаем
  add         low_z

  ; делаем uppercase
  sub         low_a
  add         up_a
  jmp         continue

not_lower_a:
  add         low_a           ; просто вернуть как было
  jmp         continue

not_lower_z:
  add         low_z           ; тоже вернуть

continue:
  store_ind   ptr             ; записываем символ в тек. позиц буфера

  load        ptr
  add         one             ; ptr++
  store       ptr

  jmp         read_loop       ; дальше читаем


read_end:
  load        zero
  store_ind   ptr             ; ставим \0


print_buf:
  load_imm    buf
  store       ptr             ; снова с начала

print_loop:
  load_addr   ptr
  load_acc                    ; берём символ из буфера
  and         byte_mask

  beqz        end             ; если 0 - конец
  store_ind   output_ptr      ; печатаем

  load        ptr
  add         one             ; ptr++
  store       ptr

  jmp         print_loop      ; дальше печатаем


end:
  halt                        