		mov		r0, #0
		mov		r1, #0
loop
		cmp		r0, #10
		bge		fin
		add		r1, r1, r0
		add		r0, r0, #1
		b		loop
fin
