import angr
import claripy

def constraint(state, flag, start, str):
    for i in range(len(str)):
        state.solver.add(flag.get_byte(start+i) == ord(str[i]))

project = angr.Project('./john.bak', selfmodifying_code=True)
project.hook_symbol('ptrace', angr.SIM_PROCEDURES['stubs']['ReturnUnconstrained'](return_value=0))

strlen = 33

input_flag = claripy.BVS('flag', strlen * 8)

argv = [project.filename, input_flag]

state = project.factory.full_init_state(add_options=angr.options.unicorn, args=argv)

# Constrain the flag to be printable characters
for i in range(strlen):
    state.solver.add(input_flag.get_byte(i) >= 0x20)
    state.solver.add(input_flag.get_byte(i) <= 0x7e)

# Constrain the flag to begin with "flag{packer"
#constraint(state, input_flag, 0, "flag{packer")

# Constrain the flag to end with "annoying__}"
#constraint(state, input_flag, 33 - len("annoying__}"), "annoying__}")

# Find when the program prints "You got" and avoid printing "Loser"
simgr = project.factory.simulation_manager(state)

#simgr.explore(find=lambda s: b"You got" in s.posix.dumps(1))

while simgr.active:
    run = 1
    simgr.step()#run(n=run)
    if 'deadended' in simgr.stashes and simgr.deadended:
        simgr.stashes['deadended'] = simgr.deadended[-run:]
    if simgr.errored:
        simgr.errored = simgr.errored[-run:]

assert simgr.deadended
flag = simgr.deadended[-1].posix.dumps(0).split(b'\n')[0]
import ipdb; ipdb.set_trace()

print(flag)

if simgr.found:
    found = simgr.found[0]
    flag = found.solver.eval(flag, cast_to=bytes)

    print('Flag: ' + flag.decode())
else:
    print('unsat')