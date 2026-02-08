#A function that returns a value:
def get_greeting():
  return "Hello from a function"

message = get_greeting()
print(message)


#Using the return value directly:
def get_greeting():
  return "Hello from a function"

print(get_greeting())


#Functions can return values using the return statement:
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)


"""
Functions can return any data type, including lists, tuples, dictionaries, and more.
A function that returns a list:
"""
def my_function():
  return ["apple", "banana", "cherry"]

fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])



