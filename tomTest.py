# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 14:53:21 2014

@author: Thomas L. Blanchet <tlblanchet@gmail.com>
"""

##Looked up PyUnit, I don't really like it. I'm doing something that will
##do the job just fine.
import traceback

class OutputError(StandardError):
    pass

def _printInfo(t, out, passed):
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    print "Testing", t[0].func_name,
    if len(t[1])!=0 or len(t[2])!=0:
        print "with input :", 
    else:
        print ":",
    if len(t[1])!=0:
        print t[1][0],
        for v in t[1][1:]:
            print ",",
            print v,
    if len(t[2])!=0:
        for k in t[2]:
            print k, "=", t[2][k],"",
    print ""
    
    if hasattr(t[0], "output"):
        print "Expecting output :", t[0].output
    
    if out!=None:
        print "Output :", out
        
    if passed:
        print "PASSED"
        print ""
    else:
        print "FAILED"
        tb = traceback.format_exc().splitlines()
        tb = [tb[0]]+[tb[i]+"\n"+tb[i+1] for i in range(1, len(tb)-1, 2)]+[tb[-1]]
        lastRep = 0
        i = 0
        while i<len(tb):
            if tb[i] in tb[lastRep:i]:
                rep = tb[tb[lastRep:].index(tb[i]):i]
                print "-------REPEATED:-------"
                for l in rep:
                    print l
                print "..."
                print "-----------------------"
                while(tb[i] in rep):
                    i += 1
                lastRep = i
            print tb[i]
            i+= 1
        print ""
    print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
                
def Test(verbose = False, printOnlyFailure = True):
    """Run this to test all properly decorated functions."""
    errors = {}
    succeed = False
    for t in Test.tests:  
        out = None
        try:
            out = t[0](*t[1], **t[2])
            if verbose and (not printOnlyFailure):
                _printInfo(t, out, True)
            
        except OutputError as o:
            errors[str((t[0].func_name, t[1], t[2]))] = o
            out = o.args[1]
            if verbose:
                _printInfo(t, out, False)
                
        except StandardError as e:
            errors[str((t[0].func_name, t[1], t[2]))] = e
            if verbose:
                _printInfo(t, out, False)
    print "====================================="
    if len(errors) != 0:
        print "Test Failed!"
    else:
        print "Test Successful!"
        succeed = True
    print len(errors), " of ", len(Test.tests), " tests have failed."
    print "====================================="
    return succeed, errors
        
Test.tests = []##This will be the list of functions to test.
Test.testOutputs = {}##This will be the dict of expected outputs

def toTest(*args, **kwargs):
    """
    Function decorator for tests.    
    
    When Test() is run, Test() will iterate through
    all functions decorated with this decorator.
    
    usage:
    @toTest(1, 0)
    @toTest(1, 2)
    def div(a, b):
        a/b
    return
    ##...
    Test()
    #This will pass on 1, 2 and fail on 1, 0
    """
    def getToTest(function):
        Test.tests.append((function, args, kwargs))
        return function
    return getToTest
    
def inTests(func):
    """Sees if the passed function is already in Test.tests"""
    return func in [t[0] for t in Test.tests]
    
def checkIsOutput(output, *args, **kwargs):
    """
    Same as toTest, but first arguement is the expected output.
    If the output is not the passed expected output, this
    function throws an OutputError.
    """
    def getCheckIsOutput(function):
        def newFunc(*nargs, **nkwargs):
            ret = function(*nargs, **nkwargs)
            if output != ret:                   
                raise OutputError(\
                     function.func_name+" output " +str(ret)+ " not " + str(output),\
                     ret)
            return ret
        newFunc.func_name = function.func_name
        newFunc.output = output
        toTest(*args, **kwargs)(newFunc)
        return function
    return getCheckIsOutput
    
def checkIsOutInstance(cls, *args, **kwargs):
    """
    Same as toTest, but first arguement is the expeceted inhereted class.
    If the output is not inherieted from the expected class, this
    function throws an OutputError. 
    (The first arguement may also be a tuple of classes.)
    """
    def getCheckIsOutInstance(function):
        def newFunc(*nargs, **nkwargs):
            ret = function(*nargs, **nkwargs)
            if not isinstance(ret, cls):
                raise OutputError(\
                     function.func_name+" output " +str(ret)+ " not a " + str(cls),\
                     ret)
            return ret
        newFunc.func_name = function.func_name
        newFunc.output = cls
        toTest(*args, **kwargs)(newFunc)
        return function
    return getCheckIsOutInstance
    

##############EXAMPLE#############    
#@toTest()
#def divideByZero():
#    return 1/0
#
#@checkIsOutput(0, 1, 0)
#@checkIsOutput(0, 1, 2)
#@toTest(1, 1)
#@checkIsOutput(1/3., 1, 3)
#@toTest(1, 3)
#def divide(a, b):
#   return a/b