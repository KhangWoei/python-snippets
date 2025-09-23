import random
import string
import sys

def constants():
    left = "pooled"
    right = "pooled"
    
    print("(Compile time) Constant strings are pooled")
    check_identity(left, right)

def dynamic():
    random_value = random.randint(10, 100)
    left = str(random_value)
    right = str(random_value)
    
    print("(Run time) Dynamic strings are not pooled, with an exception")
    check_identity(left, right)

def dynamic_exception_length():
    random_string = ''.join(random.choice(string.ascii_letters))
    left = str(random_string)
    right = str(random_string)
    
    print("(Run time) Dynamic strings are pooled unless if the length of the string is 1")
    check_identity(left, right)

def dynamic_exception_creation():
    left =''.join(random.choice(string.ascii_letters) for _ in range(random.randint(2, 10)))
    right = str(left)
    
    print("If we try to construct a string, with a string, it will just return the original string")
    check_identity(left, right)

def interning():
    random_value = random.randint(10, 100)

    left = str(random_value)
    sys.intern(left)

    right = sys.intern(str(random_value))

    print("(Intern) Forcing python to pool a string")
    check_identity(left, right)


def check_identity(left: str, right: str):
    print(f"""
            left  = {left} (id: {id(left)})
            right = {right} (id: {id(right)})
            left is right: {left is right}
          """)

if __name__ == "__main__":
    print("Python maintains an interned strings dictionary and in some cases will store string in there for optimization purposes \n")

    constants()

    dynamic()

    dynamic_exception_length()

    dynamic_exception_creation()
    
    interning()
