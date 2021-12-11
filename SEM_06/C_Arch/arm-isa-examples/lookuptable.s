		;		lookup table for factorials.
		;
		adr		r10, data
		adr		r11, value
		ldr		r1, [r11, #0] ; r1 = 6
		mov		r1, r1, lsl #0x2 ; r1 = 6*4
		add		r10, r10, r1
		ldr		r2, [r10] ; ldr r2, [r10, r1]
		adr		r3, result
		str		r2, [r3]
		
data		dcd		1, 1, 2, 6, 24, 120, 720, 5040
value	dcd		6
result	dcd		0x0
