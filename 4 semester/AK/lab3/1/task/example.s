.data
.org 0x00
buf0: .word 0x5F5F5F5F
buf1: .word 0x5F5F5F5F
buf2: .word 0x5F5F5F5F
buf3: .word 0x5F5F5F5F
buf4: .word 0x5F5F5F5F
buf5: .word 0x5F5F5F5F
buf6: .word 0x5F5F5F5F
buf7: .word 0x5F5F5F5F

.data
.org 0x90
input_addr:     .word 0x80
output_addr:    .word 0x84

cur_word_ptr:   .word 0
byte_pos:       .word 0
remaining:      .word 31
ch:             .word 0
tmp:            .word 0
old_word:       .word 0
finalize:       .word 0

const_1:        .word 1
const_4:        .word 4
const_8:        .word 8
const_16:       .word 16
const_24:       .word 24
const_ff:       .word 0x000000FF

char_nl:        .word 10
char_a:         .word 97
range_26:       .word 26
case_diff:      .word 32

mask_b0_clear:  .word 0xFFFFFF00
mask_b1_clear:  .word 0xFFFF00FF
mask_b2_clear:  .word 0xFF00FFFF
mask_b3_clear:  .word 0x00FFFFFF

overflow_value: .word 0xCCCCCCCC

.text
.org 0x100
_start: load_imm buf0
        store_addr cur_word_ptr
        load_imm 0
        store_addr byte_pos
        load_imm 31
        store_addr remaining

read_loop: load_addr input_addr
           load_acc
           and const_ff
           store_addr ch

           load_addr ch
           sub char_nl
           beqz finish_string

           load_addr remaining
           beqz overflow

           load_addr ch
           sub char_a
           store_addr tmp
           ble not_lowercase

           load_addr tmp
           sub range_26
           ble make_upper
           jmp not_lowercase

not_lowercase: load_imm 0
               store_addr finalize
               jmp write_char

make_upper: load_addr ch
            sub case_diff
            store_addr ch
            load_imm 0
            store_addr finalize
            jmp write_char

finish_string: load_imm 0
               store_addr ch
               load_imm 1
               store_addr finalize
               jmp write_char

overflow: load_addr overflow_value
          store_ind output_addr
          halt

write_char: load_addr cur_word_ptr
            load_acc
            store_addr old_word

            load_addr byte_pos
            beqz write_b0
            sub const_1
            beqz write_b1
            sub const_1
            beqz write_b2
            jmp write_b3

write_b0: load_addr old_word
          and mask_b0_clear
          store_addr tmp
          load_addr ch
          and const_ff
          or tmp
          store_ind cur_word_ptr
          jmp after_write

write_b1: load_addr old_word
          and mask_b1_clear
          store_addr tmp
          load_addr ch
          and const_ff
          shiftl const_8
          or tmp
          store_ind cur_word_ptr
          jmp after_write

write_b2: load_addr old_word
          and mask_b2_clear
          store_addr tmp
          load_addr ch
          and const_ff
          shiftl const_16
          or tmp
          store_ind cur_word_ptr
          jmp after_write

write_b3: load_addr old_word
          and mask_b3_clear
          store_addr tmp
          load_addr ch
          and const_ff
          shiftl const_24
          or tmp
          store_ind cur_word_ptr

after_write: load_addr finalize
             bnez done

             load_addr byte_pos
             add const_1
             store_addr byte_pos

             load_addr byte_pos
             sub const_4
             beqz advance_word

same_word:    load_addr remaining
              sub const_1
              store_addr remaining
              jmp read_loop

advance_word: load_imm 0
              store_addr byte_pos
              load_addr cur_word_ptr
              add const_4
              store_addr cur_word_ptr
              jmp same_word

done: halt