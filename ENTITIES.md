# Entities

## Compiler
*constrains*: a list of constrains to be solved
*optimization_constrains*: a list of constrains to optimize the final assembly

*solve()*: function to solve all the constrains 
*optimize()*: function optimize the final assembly

## Constrain
*key*: a key to be solved
*args*: list of arguments to be used when solving the constrains

### Args
*value*: value to be solved with the constrain

## Library
A library is map associating keys to collections, parts or functions that will be used to solve a constrain by mapping a name to a value. 

*_library*: map structure

*add(key, value)*: associate a key with a allowed value (e.g collection, part and function) 
*remove(key)*: remove a key
