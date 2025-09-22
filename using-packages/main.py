def print_something(input: str):
    print("Hi, {0}".format(input))

if __name__ == "__main__":
    import sys
    input = str(sys.argv[1])
    print_something(input)

