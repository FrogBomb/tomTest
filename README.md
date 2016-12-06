# tomTest
A unit testing helper for python

A spiritual precursor to lwf_test
#EXAMPLE
~~~~{.python}
import tomTest as tt
tt.clearTests() #Put in main file for testing in console
@tt.toTest()
def divideByZero():
    return 1/0

@tt.checkIsOutput(0, 1, 0)
@tt.checkIsOutput(0, 1, 2)
@tt.toTest(1, 1)
@tt.checkIsOutput(1/3., 1, 3)
@tt.toTest(1, 3)
def divide(a, b):
   return a/b
~~~~
