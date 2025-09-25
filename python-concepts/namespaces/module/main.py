variable = "sub_module"

def scopes():
    def local_scope():
        """
        In the local scope variables areread-only, attempting to write to them will create a new local variable in this scope.
        """
        variable = "sub_module_local"
        print(f"During local assignment: {variable}")

    def nonlocal_scope():
        """
        The nonlocal keyword tells python to bind to the variables foun doutside of the local scope.
        """
        nonlocal variable
        variable = "sub_module_nonlocal"
        print(f"During non local assignment: {variable}")

    def global_scope():
        """
        The global keyword tells python to bind to the outermost scope which is the module's namespace.
        """
        global variable 
        variable = "sub_module_global"
        print(f"During global assignment: {variable}")
    
    variable = "sub_module_function"
    print(f"Function initi: {variable}")

    local_scope()
    print(f"After local assignment: {variable}")

    nonlocal_scope()
    print(f"After nonlocal assignment: {variable}")

    global_scope()
    print(f"After global assignment: {variable}")
