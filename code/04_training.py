# 04_training.py
# Training: Functions in Python
# Pairs with R training:
# https://timothyfraser.com/sigma/functions-in-r.html
# Tim Fraser

# Coding your own function! #######################

# Make function
def add(a,b):
  # Compute and directly output
  return a + b

add(1,2)

# This also works
def add(a, b):
  # Assign output to a temporary object
  output = a + b
  # Return the temporary object 'output'
  return output
# 
add(1, 2)

# Functions with default inputs #####################

# try adding a default value of 2 for b
def add(a, b = 2):
  return a + b
# See? I only need to write 'a' now
add(1)


# But if I write 'b' too...
add(1,2)


# And if I change 'b'...
add(1,3)


# It will adjust accordingly

# clear data
del add

# Conclusion ####################

# Great! Let’s go make some functions!


