variable = "scopes module"

class Scopes:
    variable = "class" #this is a class variable, it is static 

    def local_scope(self):
        variable = "class local"
        print(f"During local assignment: {variable}")

    def nonlocal_scope(self):
        """
        Lexical scoping only applies to function namespaces, to prevent methods inside a class from 
        seeing class level attributes.
        """
        self.variable = "class nonlocal"
        print(f"During non local assignment: {self.variable}")

    def global_scope(self):
        global variable
        variable = "class global"
        print(f"During global assignment: {variable}")

    def print_variable(self):
        print(f"After: {self.variable}")

    def scopes(self):
        self.print_variable()

        self.local_scope()
        self.print_variable()

        self.nonlocal_scope()
        self.print_variable()

        self.global_scope()
        self.print_variable()
