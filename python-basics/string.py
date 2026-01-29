#length of the string
a = "Hello, World!"
print(len(a))   


#checking in sthe string
txt = "The best things in life are free!"
print("free" in txt)


#slicing
b = "Hello, World!"
print(b[2:5]) #from 2, to 4(include)

b = "Hello, World!"
print(b[:5]) #from the start to 4(included)

b = "Hello, World!"
print(b[2:])#from 2 to the end

b = "Hello, World!"
print(b[-5:-2]) #from index -5 to -3


#modifying
a = "Hello, World!"
print(a.upper())#in the upper case HELLO WORLD

a = "Hello, World!"
print(a.lower())#in the lower case hello world

a = " Hello, World! "
print(a.strip()) # returns "Hello, World!"

a = "Hello, World!"
print(a.replace("H", "J")) #Jello, World!


a = "Hello, World!"
print(a.split(",")) # returns ['Hello', ' World!']

#concatenation
a = "Hello"
b = "World"
c = a + b
print(c) 


#format string

age = 36
txt = f"My name is John, I am {age}"
print(txt)

price = 59
txt = f"The price is {price} dollars"
print(txt)


price = 59
txt = f"The price is {price:.2f} dollars"
print(txt)


txt = f"The price is {20 * 59} dollars"
print(txt)

'''
Escape Characters

\'	Single Quote	
\\	Backslash	
\n	New Line	
\r	Carriage Return	
\t	Tab	
\b	Backspace	
\f	Form Feed	
\ooo	Octal value	
\xhh	Hex value
'''


'''
upper()	Converts a string into upper case

split()	Splits the string at the specified separator, and returns a list

replace()	Returns a string where a specified value is replaced with a specified value

lower()	Converts a string into lower case

isupper()	Returns True if all characters in the string are upper case

islower()	Returns True if all characters in the string are lower case

isdecimal()	Returns True if all characters in the string are decimals

isdigit()	Returns True if all characters in the string are digits

index()	Searches the string for a specified value and returns the position of where it was found

isalnum()	Returns True if all characters in the string are alphanumeric

isalpha()	Returns True if all characters in the string are in the alphabet

find()	Searches the string for a specified value and returns the position of where it was found

count()	Returns the number of times a specified value occurs in a string
'''