import types
from typing import List
from dnacompiler.Constrain import Constrain
from dnacompiler.Library import Library
from dnacompiler.Part import Part
from dnacompiler.Sequence import Sequence

class Compiler():
  _library: Library 

  def __init__(self, constrains, optimization_constrains = {}):
    self._constrains = self._list_to_constrains(constrains)
    self._optimization_constrains = self._list_to_constrains(optimization_constrains)

  def build(self) -> List[Sequence]:
    # TODO: Check if library exist and if library.keys > 0. If not raise an error
    sequence = []
    for constrain in self._constrains:
      part_solved = self._solve(constrain)
      if type(part_solved) != str and not isinstance(part_solved, list):
        raise TypeError
      if isinstance(part_solved, list):
        sequence.append(Part(constrain.name, part_solved, 'combinatorial'))
      else:
        sequence.append(Part(constrain.name, part_solved.upper()))

    sequences = []
    for parts in self._optimize(sequence):
      sequences.append(Sequence(parts))

    return sequences

  def _optimize(self, parts: List[Part]) -> List[List[Part]]:
    sequences = []
    for part in parts:
      sequences = self._comb_solve(part, sequences)

    optimized = []
    for sequence in sequences:
      for opt_constrain in self._optimization_constrains:
        func_solved = self._solve(opt_constrain)
        optimized.append(func_solved(sequence))
      
    if len(optimized) > 0:
      return optimized

    return sequences
    
  def _comb_solve(self, part, sequences):
    # TODO: URGENT! This code is a piece of garbage completely. REFACTOR!
    local = []
    if len(sequences) == 0:
      if isinstance(part.value, list):
        if len(part.value) > 1:
          for element in part.value:
            # TODO: get from dictionary is not a good practice - improve a logic for combinatorial sequences
            local.append([Part(element.get('name'), element.get('value'), part.partType)])
          return local
        local.append([Part(part.name, part.value[0].value, part.partType)])
        return local
      return [[part]] 
    else:
      if isinstance(part.value, list):
        if len(part.value) > 1:
          for element in part.value:
            for sequence in sequences:
              # TODO: get from dictionary is not a good practice - improve a logic for combinatorial sequences
              local.append(sequence + [Part(element.get('name'), element.get('value'), part.partType)])
          return local
        for sequence in sequences:
          local.append(sequence + [Part(part.name, part.value[0].value, part.partType)])
        return local
      for sequence in sequences:
        local.append(sequence + [part])
      return local 
  
  def _solve(self, constrain):
    value = self._library.get(constrain.name)
    if type(value) == types.FunctionType:
      if constrain.args != None:
        return value(constrain.args)
      return value()
    return value

  def _dict_to_constrain(self, value: dict) -> Constrain:
    if 'constrain' in value:
      if 'args' in value:
        return Constrain(value['constrain'], value['args'])
      return Constrain(value['constrain'], None)
    else:
      raise KeyError

  def _list_to_constrains(self, value: list):
    constrains = []
    for obj in value:
      constrains.append(self._dict_to_constrain(obj))
    return constrains

  def setLibrary(self, library: Library) -> None:
    self._library = library
