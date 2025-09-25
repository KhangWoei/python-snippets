def scopes():
    def local_scope():
        """
        In the local scope variables areread-only, attempting to write to them will create a new local variable in this scope.
        """
        variable = "local"
        print(f"During local assignment: {variable}")

    def nonlocal_scope():
        """
        The nonlocal keyword tells python to bind to the variables foun doutside of the local scope.
        """
        nonlocal variable
        variable = "nonlocal"
        print(f"During non local assignment: {variable}")

    def global_scope():
        """
        The global keyword tells python to bind to the outermost scope which is the module's namespace.
        """
        global variable 
        variable = "global"
        print(f"During global assignment: {variable}")
    
    variable = "function"
    print(f"Function initi: {variable}")

    local_scope()
    print(f"After local assignment: {variable}")

    nonlocal_scope()
    print(f"After nonlocal assignment: {variable}")

    global_scope()
    print(f"After global assignment: {variable}")

if __name__ == "__main__":
    variable = "module"
    print(f"Module init: {variable}")

    scopes()
    print(f"Global scope: {variable}")

