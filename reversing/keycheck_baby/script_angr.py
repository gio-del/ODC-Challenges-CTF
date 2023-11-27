import angr
import claripy

strlen = 31

prog = angr.Project('./keycheck_baby')

input_flag = claripy.BVS('flag', 8 * strlen)

state = prog.factory.full_init_state(stdin=input_flag, add_options={angr.options.LAZY_SOLVES})

for i in range(strlen-1):
	state.add_constraints(input_flag.get_byte(i) >= 0x20, input_flag.get_byte(i) <= 0x7f)

state.add_constraints(input_flag.get_byte(0) == ord('f'))
state.add_constraints(input_flag.get_byte(1) == ord('l'))
state.add_constraints(input_flag.get_byte(2) == ord('a'))
state.add_constraints(input_flag.get_byte(3) == ord('g'))
state.add_constraints(input_flag.get_byte(4) == ord('{'))
state.add_constraints(input_flag.get_byte(strlen-1) == ord('}'))

simgr = prog.factory.simulation_manager(state)
simgr.explore(find=lambda s: b"Your input" in s.posix.dumps(1))

if simgr.found:
	s = simgr.found[0].solver

	flag = s.eval(input_flag)
	flag = bytes.fromhex(hex(flag)[2:]).decode('utf-8')

	print(flag)
else:
	print('unsat')