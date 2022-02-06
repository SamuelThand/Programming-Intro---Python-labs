# Laboration 2

## Environment & Tools
Ubuntu 20.04 LTS, Pycharm 2021.2.1, Python 3.8.10, Git 2.25.1

## Purpose

This assignment aims to help the student understand the usage of strings, string slicing, string methods such as 
capitalize(), string formatting, parsing and iteration through strings, the usage of functions, function definition with parameters, type hints and annotations,
function calling and understanding of scope within and outside functions. Running python programs with arguments 
and user input, interaction and validation.

##Procedures

### Part 1 
The solution can be reproduced by building the functions as follows.

#### authenticate_user()
Parsing the input string inside the authenticate_user function 
into a list for the username, and a string for the password
using string method split() with a blank space separator ' ', and
string slicing for the username and string indexing for the password.
Assign values into temporary variables user_tmp, pass_tmp. 
Call functions format_username and decrypt_password within authenticate_user
function and assign return value into temporary variables user_tmp, pass_tmp. 
Return the boolean value of a compound statement testing IF
the value in user_tmp exists as a key in agents dictionary, AND if the 
value of key user_tmp is equal to pass_tmp.
#### format_username()
Use indexing on incoming list value to extract the string values
and capitalize it with string method capitalize(). Store values in variables
for given and sur name. Glue together capitalized given and sur name with a _ using string
formatting. Store new string in variable for formatted username and return formatted username to authenticate_user().
#### decrypt_password()
Write a loop iterating through the characters of incoming string value
and keep track of the iteration count using enumerate(). Determine if iteration count is even or odd using conditional statements.
Convert character to unicode integer using ord() and add integer value
of rot7 for even count values and rot9 for odd count values. Assign integer to tmp variable.
Convert integer stored in tmp to unicode character string using chr() and
assign value to new_char variable.
Determine if character is a substring of vowels variable. If true, 
add '0' character before and after character using string formatting. Assign value to new_char variable.
Append character to a new string and assign to decrypted variable. Repeat these steps for all characters.
Return decrypted variable to authenticate_user().
### Problems

Problems arose from confusion when jumping between functions and trying
to determine the flow of execution. This was
resolved by appropriate use of scaffolding with print statements clearly
showing what took place and where. Initial use of stepping function
in the pycharm debugger also helped show the flow of execution in the program
helping with understanding of the assignment. 

Initial information overflow from the assignment caused problems, but
they were resolved from methodical procedure and splitting of the assignment
into smaller mini-assignments. 


## Discussion

### Perspective

I think the purpose has been fulfilled. The assignment prompted further
research and using the tools we have read about in the course material, and also
introduced more methodical considerations such as scaffolding,
debugging and best practices for avoiding unnessecary headaches.

I think the implementation was suitable, and at this moment I don't think
an alternative approach is to be considered. 

###Personal reflections
I got much practice in using scaffolding, debugging and a step-by-step
coding process which made the procedure cause less friction.

I found the function defining intermediately difficult, while keeping
a structured approach was the bigger challenge. 






