def main(input: str):
    """
    Hi from main's doc string
    """
    print("Hi, {0}".format(input))

if __name__ == "__main__":
    import sys
    import simple_package
    import simple_package.submodule

    input = str(sys.argv[1])

    main(input)
    print(main.__doc__)

    simple_package.main(input)
    simple_package.submodule.main(input)

