  .data
buf:          .byte '________________________________'
buf_end:         .byte '___'
zero:       .byte '\0___'

input_ptr:      .word  0x80
output_ptr:     .word  0x84

ptr:               .word  0
newline:         .word  '\n'
one:       .word  1
byte_mask:            .word  0xFF
low_a:         .word  'a'
low_z:         .word  'z'
up_a:         .word  'A'
overflow:   .word  0xCCCC_CCCC


  .text

.org 0x88

overflow_err:
  load          overflow
  store_ind     output_ptr
  jmp end

_start:
read_string:
  load_imm      buf          ;   acc = buf
  store         ptr               ;   ptr = buf
  
read_loop:
  load_imm      buf_end
  sub           ptr               ;  ptr == &buf_end или переполнение err
  beqz          overflow_err
  load_addr     input_ptr   ;   acc = mem[input_ptr] = 0x80
  load_acc                   ;   acc = mem[acc] = mem[0x80]
  and           byte_mask            ;    acc & 0xFF
  sub           newline         ;   acc - '\n'
  beqz          read_end        ;  acc == '\n' если да, то завершаем работу
  add           newline         ;   восстанавливаем acc

  sub           low_a         ; c -= 'a'
  ble           not_lower_a     ; c < 'a' ? => not_lower
  add           low_a         ; восстанавливаем c 
  sub           low_z         ; c -= 'z'
  bgt           not_lower_z     ; c >'z' => not_lower
  add           low_z
  sub           low_a
  add           up_a         ; c += 'A' (в верхнем регистре)
  jmp           continue

not_lower_a:
  add           low_a
  jmp           continue

not_lower_z:
  add           low_z

continue:
  store_ind     ptr               ; buf[ptr] = acc
  load          ptr               ; acc = ptr
  add           one       ; ptr++
  store         ptr
  jmp           read_loop       ; следующая итерация

read_end:
  load          zero
  store_ind     ptr

print_buf:
  load_imm      buf          ; acc = buf
  store         ptr               ; ptr = buf

print_loop:
  load_addr     ptr
  load_acc
  and           byte_mask            ; c & 0xFF (обрезаем до байта)
  beqz          end             ; c == '\0' - конец строки
  store_ind     output_ptr     ; c -> stdout
  load          ptr               ; acc = ptr
  add           one       ;   ptr++
  store         ptr               ; сохраняю значение указателя ptr
  jmp           print_loop      ; следующая итерация


end:

  halt