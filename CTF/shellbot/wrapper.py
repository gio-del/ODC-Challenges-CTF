from subprocess import run
import sys

def main():
    print("My name is ShellBot, and I'm a nice bot.")
    print("I will try to execute your shellcode, but I'm not sure if it will work.")
    print("The guy who made me is a bit lazy, so I don't know how to execute some of the instructions.")
    print("You'll need to send me the shellcode in hex format")
    print("How long is your shellcode? ")

    length = int(input())
    print("Give me your shellcode (hex-formatted): ")

    num_bytes = 0
    read_bytes = ""

    while(num_bytes < length):
        read_bytes += sys.stdin.read(length - num_bytes)
        num_bytes += len(read_bytes)

    shellcode = bytes.fromhex(read_bytes)

    if b"\x0f\x05" in shellcode or b"\x48\xc7" in shellcode:
        print("Nope.")
        sys.exit(1)
    else:
        print("Let's see...")
        run(["./shellbot"], input=shellcode)
    
if __name__ == "__main__":
    main()

