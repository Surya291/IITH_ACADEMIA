			;		multiply two registers values
			;		r0 = r0 * r1, both 16 bit numbers
			;		r8-r11 are scratch registers
			;		result comes back in r0
			mov		r0, #0x100
			mov		r1, #0x03
			bl		mult
			b		halt
			
mult
			stmea	sp!, {lr} ; stack grows upwards
			mov		r8, #0x10  ; how many bits
			mov		r9, #0x0   ; loop counter
			mov		r10, #0x1   ; mask
			mov		r11, #0x0   ; tmp result
shift_and_add
			tst		r1, r10, lsl r9 ; check if a bit is set in r1
			addne	r11, r11, r0, lsl r9 ; add if the bit was set
			add		r9, r9, #0x1
			cmp		r9, r8
			bne		shift_and_add
			mov		r0, r11
			ldmea	sp!, {pc}
			
halt
