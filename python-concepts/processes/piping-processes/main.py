import os
import sys

r, w = os.pipe()

writer = os.fork()

if (writer != 0):
    reader = os.fork()

    if (reader == 0):
        os.dup2(r, sys.stdin.fileno())
        
        pipedInput = input()
        print(f"{os.getpid()} received: {pipedInput}")
else:
    os.dup2(w, sys.stdout.fileno())
    print(f"{os.getpid()} says hi")
