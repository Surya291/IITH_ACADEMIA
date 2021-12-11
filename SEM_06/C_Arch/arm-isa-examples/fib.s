		;		recursive fibonacci
		;		r1 has "n", r0 should have fib(n)
		;		fib(n) = fib(n-1) + fib(n-2)
		mov		r1, #0x7
		bl		fib
		b		halt
fib
		stmea	sp!, {r1, lr}
		mov		r0, #0x1
		cmp		r1, #0x1
		beq		return ; if n==1 or n==0 then return with r0=1
		cmp		r1, #0x0
		beq		return
				; calculate fib(n-2)
		stmea	sp!, {r1} ; make a copy of n (i.e. r1)
		sub		r1, r1, #0x2
		bl		fib
		ldmea	sp!, {r1}	; restore n (i.e. r1)
		stmea	sp!, {r0}	; make a copy of fib(n-2)
				; calc fib(n-1)
		sub		r1, r1, #0x1
		bl		fib
		ldmea	sp!, {r2} ; bring fib(n-2) to r2
		add		r0, r0, r2 ; add fib(n-1) to fib(n-2) and leave in r0
return
		ldmea	sp!, {r1, pc}
halt
