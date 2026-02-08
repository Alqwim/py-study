class Flyer:
    def fly(self):
        print("I can fly")


class Swimmer:
    def swim(self):
        print("I can swim")


class Duck(Flyer, Swimmer):
    def sound(self):
        print("Quack!")
# This example demonstrates multiple inheritance in Python.
# The Duck class inherits methods from both Flyer and Swimmer classes.