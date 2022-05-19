# rpn-esolang
(working title)
A prototype esoteric programming language based on Reverse Polish Notation.

This is a prototype subject to change, I do not know whether it is turing complete.

## Language details:
NOTE: EVERYTHING IS HIGHLY EXPERIMENTAL AND WILL AMOST CERTAINLY BE CHANGED

Each line of a source file contains one element, they can be any of the following:

- Number : real number represented in base 10
- String : any string notated using single or double quotes
- \+ : addition operation
- \- : subtraction operation
- \* : multiplication operation
- / : division operation
- = : equality
- < : less than
- \> : more than
- <= : less than or equal
- \>= : more than or equal
- [offset] : copy the element at the stack offset
- << : print the last element and pop

It is currently undefined what happens when trying to use mathematical operations on strings, details on this will be worked on and refined as I develop this further.
