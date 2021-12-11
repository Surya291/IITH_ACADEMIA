		;		floating point addition, m is bits 0-22, e is bits 23-30, bit 31 is sign
		;		r0 = 1.m0 x 2^e0
		;		r1 = 1.m1 x 2^e1
		;		let e0 be less than e1
		;		scale m0 so that e0 becomes equal to e1
		;		add or subtract m1 and m0
		;		normalise
		
		;		move numbers into registers
		adr		r12, f1
		ldr		r0, [r12]
		ldr		r1, [r12, #4]
fpadd
		;		extract e0, e1, swap them if e0 is bigger
		lsr		r8, r0, #23
		lsr		r9, r1, #23
		cmp		r8, r9
		movgt	r2, r0
		movgt	r0, r1
		movgt	r1, r2
		
		
		
f1		dcd		0x3fe00000  ; 1.75
f2		dcd		0x3fa00000	 ; 1.25
f3		dcd		0xbfa00000  ; -1.25
mask		dcd		0xff800000	 ; mask to extract m
