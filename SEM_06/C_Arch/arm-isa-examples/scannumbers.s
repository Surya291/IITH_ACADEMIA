		; scan numbers to count how many are -ve (16 bits)
		adr		r10, table
		adr		r11, tablend
		adr		r12, length
		sub		r2, r11, r10
		mov		r2, r2, lsr #0x2
		str		r2, [r12]
		eor		r1, r1, r1
		cmp		r2, #0x0
		beq		done
loop
		ldr		r3, [r10]
		and		r3, r3, #0x8000
		cmp		r3, #0x8000
		bmi		looptest
		add		r1, r1, #1
looptest
		add		r0, r0, #+0x4
		subs		r2, r2, #0x1
		bne		loop
done
		adr		r4, result
		str		r1, [r4]
		
		
		
table	dcd		0xa152, 0x7561, 0xf123, 0x0080
tablend	dcd		0x0
		
length	dcd		0x0
result	dcd		0x0
