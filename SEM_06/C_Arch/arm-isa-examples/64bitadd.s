		;		64 bit addition
		;		v1: 12A2E640,F2100123
		;		v2: 001019BF,40023F51
		;		sum: 12B30000,32124074
		
		adr		r0, val1  ; mov r0, #0x100    imm constant for mov 22 bits
		;		add r0, pc, 0x100
		ldmia	r0, {r1, r2} ; load multiple
		adr		r0, val2
		ldmia	r0, {r3, r4} ; both of them in r1-r2 and r3-r4
		adds		r6, r2, r4 ; suffix "s"? update the carry bit
		adc		r5, r1, r3 ; use the carry bit
		adr		r0, result
		stmia	r0, {r5, r6}
		
val1		dcd		0x12A2E640, 0xf2100123
val2		dcd		0x001019bf, 0x40023f51
result	dcd		0x0
