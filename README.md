# Offensive and Defensive Cybersecurity

This repository contains the solution for various Capture The Flag (CTF) challenges taken during the Offensive and Defensive Cybersecurity Course at Politecnico di Milano along with their writeups.

Challenges are divided into categories, each one of them has its own folder. Each challenge contains a `README.md` file with the description of the challenge and the writeup.

## 🎯 Goals

The objective of the challenges is to find the flag, which is a string that follows the format `FLAG{...}`.
Each challenge has its own flag, and the goal is to find it, either by exploiting a vulnerability, reverse engineering, or by any other means.
The challenges are designed to cover a wide range of topics, from binary exploitation (ROP, heap, shellcode crafting, mitigations bypass, packing, reverse engineering, symbolic execution) to web security (race conditions, serialization, XSS).

## 🛠️ Tools

The tools used to solve the challenges are mainly:

- [GDB](https://www.gnu.org/software/gdb/)
- [pwndbg](https://www.github.com/pwndbg/pwndbg)
- [Pwntools](https://www.github.com/Gallopsled/pwntools)
- [python](https://www.python.org/)
- [IDA](https://www.hex-rays.com/products/ida/)
- [Ghidra](https://www.ghidra-sre.org/)
- [z3](https://www.github.com/Z3Prover/z3)
- [angr](https://www.github.com/angr/angr)

## 📚 Categories

- [Shellcode](./shellcode/)
- [Reverse Engineering](./reversing/)
- [Mitigation Bypass](./mitigations/)
- [ROP](./rop/)
- [Heap Exploitation](./heap/)
- [Symbolic Exeuction and Fuzzing](./symbolic/)
- [Race Condition](./race/)
- [Serialization](./serialization/)
- [XSS](./xss/)
- [Packing](./packing/)

## 📝 Final CTF

The final CTF is a timed event (9 hours) where students have to solve as many challenges as possible. The challenges are divided into the same categories as the ones in this repository.
Mine final CTF writeups are available in the [CTF](./CTF/) folder.

## 📜 License

This repository is licensed under the [MIT License](./LICENSE).

## 📧 Contact

For any questions, feedback, or suggestions, feel free to contact me. See my [GitHub profile](https://www.github.com/gio-del)
