#Return an iterator from a tuple, and print each value:
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))


#Iterate the values of a tuple:
mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x)


#Create an iterator that returns numbers, starting with 1, and each sequence will increase by one (returning 1,2,3,4,5 etc.):
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    x = self.a
    self.a += 1
    return x

myclass = MyNumbers()
myiter = iter(myclass)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))


#Stop after 20 iterations:
class MyNumbers:
  def __iter__(self):
    self.a = 1
    return self

  def __next__(self):
    if self.a <= 20:
      x = self.a
      self.a += 1
      return x
    else:
      raise StopIteration

myclass = MyNumbers()
myiter = iter(myclass)

for x in myiter:
  print(x)


#simple example of generator:
def my_generator():
    yield 1
    yield 2
    yield 3
gen = my_generator()

print(next(gen))  # 1
print(next(gen))  # 2
print(next(gen))  # 3


#If a function has yield → it automatically becomes a generating function:
def count_up_to(n):
    i = 1
    while i <= n:
        yield i
        i += 1
for num in count_up_to(5):
    print(num)


#Generator Expressions-it's like list comprehension, but in parentheses:
nums = (x * 2 for x in range(5))