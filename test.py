print("OK")

class Animal(object):
    """Class defining animals
    """

    def __init__(self, name):
        """Initilises the animal beast

        Arguments:
        - `name`: Name of the anmal
        """
        self.name = name

    def __str__(self):
        """Prints animal in user friendly form.
        """

        return self.__class__.__name__+"(name="+self.name+")"


a=Animal("Kivi")
print (a)
quit()
