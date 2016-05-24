# tomTest
A unit testing helper for python

#EXAMPLE
~~~~{.python}
clearTests() #Put in main file for testing in console
@toTest()
def divideByZero():
    return 1/0

@checkIsOutput(0, 1, 0)
@checkIsOutput(0, 1, 2)
@toTest(1, 1)
@checkIsOutput(1/3., 1, 3)
@toTest(1, 3)
def divide(a, b):
   return a/b
~~~~
