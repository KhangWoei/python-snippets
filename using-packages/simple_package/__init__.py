def main(input: str):
    print("Simple package: {0}".format(input))

"""
    This attribute defines the modules that should be imported for `import *`
    If this is empty, only the contents of this file will be executed and imported.
"""
__all__ = ["submodule"]
