import angr
import claripy
from pwn import *

strlen = 30

prog = angr.Project('./prodkey')

find = [0x00400e58] # key ok
avoid = [0x00400e92] # key ko

input_flag = claripy.BVS('flag', strlen * 8)

state = prog.factory.entry_state(stdin=input_flag)
simgr = prog.factory.simulation_manager(state)

simgr.explore(find=find, avoid=avoid)

if simgr.found:
	found = simgr.found[0]
	flag = found.solver.eval(input_flag)
	flag = bytes.fromhex(hex(flag)[2:]).decode('utf-8')

	print('flag:', flag, 'len: ')

	p = remote("bin.training.offdef.it", 2021)

	p.recvuntil(b'\nPlease Enter a product key to continue: \n')
	p.sendline(flag)

	print('Flag:', str(p.recv(),'utf-8'))




