main
			adr		r1, hdigit
			ldr		r0, [r1]
			bl		func
			adr		r1, result
			str		r0, [r1]
			bl		stop
func
; adds 2 if r0 <= 0xa
; adds 3 if r0 > 0xa
			cmp		r0, #0x0a
			ble		next
			add		r0, r0, #0x1
next
			add		r0, r0, #0x2
			mov		pc, lr

hdigit		dcd		0xb
result		dcd		0x0

stop
