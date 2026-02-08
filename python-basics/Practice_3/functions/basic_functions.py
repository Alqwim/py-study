#To call a function, write its name followed by parentheses:
def my_function():
  print("Hello from a function")

my_function()


#You can call the same function multiple times:
def my_function():
  print("Hello from a function")

my_function()
my_function()
my_function()


def fahrenheit_to_celsius(fahrenheit):
  return (fahrenheit - 32) * 5 / 9

print(fahrenheit_to_celsius(77))
print(fahrenheit_to_celsius(95))
print(fahrenheit_to_celsius(50))