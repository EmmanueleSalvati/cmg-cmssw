#!/bin/env python

#define here all the helpers function that may be of some use for tree making

def var( tree, varName, type=float ):
    tree.var(varName, type)

def fill( tree, varName, value ):
    tree.fill( varName, value )
