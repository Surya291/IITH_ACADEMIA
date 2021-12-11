		;		alternative to using the stack pointer
		mov		r12, #0x1000  ; our stack pointer
		mov		r0, #3
		bl		mult4   ; call function mult4, save address
		;		of next instruction to lr (r14)
		b		halt
		;		i=increasing, d=decreasing, a=after, b=efore,
		;		e=empty, f=filled, a=ascending, d=descending
mult4
		stmfa	sp, {lr} ; stack grows upwards
		;		str		lr, [r12]
		;		add		r12, r12, #4
		bl		mult2
		bl		mult2
		ldmea	sp, {pc}
		;		sub		r12, r12, #4
		;		ldr		pc, [r12, #0]
mult2
		stmea	sp!, {lr}
		;		str		lr, [r12, #0]
		;		add		r12,r12, #4
		add		r0, r0, r0
		;		sub		r12, r12, #4
		;		ldr		pc, [r12, #0]
		ldmea	sp!, {pc}
		
halt
