def main(input: str):
    print("Hi, {0}".format(input))

if __name__ == "__main__":
    import sys
    import simple_package
    import simple_package.submodule
    input = str(sys.argv[1])
    main(input)
    simple_package.main(input)
    simple_package.submodule.main(input)

