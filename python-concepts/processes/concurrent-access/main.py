import os

file = open("concurrent.txt", "w")

child = os.fork()

if (child == 0):
    file.write("Child reporting")
    file.close()
else:
    file.write("Parent reporting")
    file.close()

