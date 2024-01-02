import angr
import claripy
import math

# import logging
# logging.getLogger('angr').setLevel('DEBUG')

find = [0x0804983e]
avoid = [0x08049850]
check5 = 0x080495e4
#check5 = 0x0804945e # inner

strlen = 33

def constraint(state, flag, start, str):
    for i in range(len(str)):
        state.solver.add(flag.get_byte(start+i) == ord(str[i]))

class hook_check5(angr.SimProcedure):
    def run(self):
        print("Hooked check5")
        state.regs.eax = claripy.BVV(1, 32) # Always return 1, we already found that part of the flag

project = angr.Project('./john_unpack_working', load_options={"auto_load_libs": True})#, selfmodifying_code=True, )
#project.hook_symbol('ptrace', angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained'](return_value=0))

# Hook address of check5 function
project.hook(check5, hook_check5(), length=198)
#project.hook(check5, angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained'](return_value=1), length=198)

input_flag = claripy.BVS('flag', 8 * strlen)

argv = [project.filename, input_flag]

state = project.factory.entry_state(args=argv, add_options={angr.options.ZERO_FILL_UNCONSTRAINED_MEMORY, angr.options.ZERO_FILL_UNCONSTRAINED_REGISTERS}) #add_options=angr.options.unicorn) #

# Constrain the flag to be printable characters
for i in range(strlen):
    state.solver.add(input_flag.get_byte(i) >= 0x20)
    state.solver.add(input_flag.get_byte(i) <= 0x7e)

# Constrain the flag to contain "-4_3-1337&-" from the index 11
#constraint(state, input_flag, 11, "-4_3-1337&-")

# Constrain the flag to begin with "flag{packer"
#constraint(state, input_flag, 0, "flag{packer")

# Constrain the flag to end with "annoying__}"
#constraint(state, input_flag, 33 - len("annoying__}"), "annoying__}")

simgr = project.factory.simulation_manager(state)

# Find when the program prints "You got" and avoid printing "Loser"
simgr.explore(find=lambda s: b"You got" in s.posix.dumps(1))# find, avoid=avoid) #

if simgr.found:
    found = simgr.found[0]
    flag = found.solver.eval(input_flag, cast_to=bytes)

    print('Flag: ' + flag.decode())
else:
    print('unsat')

print(simgr)
print(simgr.deadended[0])
# import pprint; pprint.pprint(state.history.descriptions.hardcopy)