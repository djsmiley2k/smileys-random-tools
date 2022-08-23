#!/usr/bin/python

# Print numbers 1 to 10 in random order
# Tim Bowers
# Sept 2020

# Import python random module
import random


# Put the numbers in a list

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print("Original list: %s." % numbers)

# Shuffles in place, returns None
random.shuffle(numbers)

# Print on a single line
print("--------------")
print("Random numbers: %s." % numbers)
print("--------------")

