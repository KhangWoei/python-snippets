import os
import stat
import datetime
import sys

parent = os.getpid()
print(f"""
       {datetime.datetime.now()} parent pid: {os.getpid()}
       """)
'''
os.fork() will spawn a new process and return that process' id to the parent.

The child process will come to life and start running from os.fork(), and will get a return result of 0 from os.fork()

Child process will get it's own private (?) address space, registers, PC, basically it's own CONTEXT based off the parent's existing context so it will still capture things declared/assigned before the fork() call.

The process that runs first is non-deterministic, so, given an environment with just one process either the parent or child could run first, however this can be meddled with using the CPU scheduler
'''
child = os.fork()

if (child < 0):
    raise Exception("fork failed")

if (child == 0):
    print(f"""
           {datetime.datetime.now()} child 
           pid: {os.getpid()}
           (captured) parent pid: {parent}
           (captured) child pid: {child}
           """)
    fd = os.open("child-process.output", os.O_CREAT | os.O_WRONLY | os.O_TRUNC, stat.S_IRWXU)
    os.dup2(fd, sys.stdout.fileno())
    os.close(fd)
    """
    Overwrites the current code segment with the for the code of the executable to run, re-initializes the resources of the current context and runs the program on the current pocess.

    So we can never return from an exec call, any code that comes after the exec call is unreachable
    """
    os.execvp("wc", ["wc", "main.py"])
    print(f"This doesn't get run as the process was replaced with another one")
else:
    """
    will wait for the child process to finish before doing anything.
    returns (child_pid, exit_status)
    """
    child_results = os.wait()
    print(f"""
           {datetime.datetime.now()} parent 
           pid: {os.getpid()}
           (captured) parent pid: {parent}
           (captured) child pid: {child}
           child results: {child_results}
           """)

