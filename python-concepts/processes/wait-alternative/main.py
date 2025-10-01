import os 


child = os.fork()

if child == 0:
    file = open("blocking.txt", "w")
    file.write("Go!")
    file.close()

    print("First!")
else:
    file = open("blocking.txt", "r")
    while True:
        line = file.read()
        
        if line:
            break
    file.close()

    print("Second!")

