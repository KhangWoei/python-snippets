def mutable_default(array: list = []):
    """
    Defaults are evaulated once during runtime, 
    when function definition is met, 
    and they are reused for the lifetime of an application.
    """
    array.append(len(array))
    print(array)

if __name__ == "__main__":
    import sys

    print(mutable_default.__doc__)
    
    input = int(sys.argv[1])
    for i in range(input):
        mutable_default()

