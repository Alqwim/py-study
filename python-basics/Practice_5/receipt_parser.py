#Import the re module:
import re


#Search the string to see if it starts with "The" and ends with "Spain":
import re

txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)


"""
The re module offers a set of functions that allows us to search a string for a match:
Function	Description
findall	    Returns a list containing all matches
search	    Returns a Match object if there is a match anywhere in the string
split	    Returns a list where the string has been split at each match
sub	        Replaces one or many matches with a string
"""


"""
Metacharacters are characters with a special meaning:
Character	Description	           Example	
[]	        A set of characters	   "[a-m]"	
\	        Signals a special sequence (can also be used to escape special characters)	   "\d"	
.	        Any character (except newline character)	   "he..o"	
^	        Starts with	    "^hello"	
$	        Ends with	    "planet$"	
*	        Zero or more occurrences	   "he.*o"	
+	        One or more occurrences	       "he.+o"	
?	        Zero or one occurrences	       "he.?o"	
{}	        Exactly the specified number of occurrences	       "he.{2}o"	
|	        Either or	                   "falls|stays"	
()	        Capture and group
"""

#Print a list of all matches:
import re

txt = "The rain in Spain"
x = re.findall("ai", txt)
print(x)


#Return an empty list if no match was found:
import re

txt = "The rain in Spain"
x = re.findall("Portugal", txt)
print(x)



#Search for the first white-space character in the string:
import re

txt = "The rain in Spain"
x = re.search("\s", txt)

print("The first white-space character is located in position:", x.start())


#Make a search that returns no match:
import re

txt = "The rain in Spain"
x = re.search("Portugal", txt)
print(x)


#Split at each white-space character:

import re

txt = "The rain in Spain"
x = re.split("\s", txt)
print(x)


#Split the string only at the first occurrence:



import re

txt = "The rain in Spain"
x = re.split("\s", txt, 1)
print(x)



#Replace every white-space character with the number 9:

import re

txt = "The rain in Spain"
x = re.sub("\s", "9", txt)
print(x)



#Replace the first 2 occurrences:

import re

txt = "The rain in Spain"
x = re.sub("\s", "9", txt, 2)
print(x)




#Do a search that will return a Match Object:

import re

txt = "The rain in Spain"
x = re.search("ai", txt)
print(x) #this will print an object




#Print the position (start- and end-position) of the first match occurrence.

#The regular expression looks for any words that starts with an upper case "S":

import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.span())



#Print the string passed into the function:

import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.string)



#Print the part of the string where there was a match.

#The regular expression looks for any words that starts with an upper case "S":

import re

txt = "The rain in Spain"
x = re.search(r"\bS\w+", txt)
print(x.group())