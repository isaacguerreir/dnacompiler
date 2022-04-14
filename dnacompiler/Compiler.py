import types
from typing import List
from dnacompiler.Constrain import Constrain
from dnacompiler.Library import Library
from dnacompiler.Part import Part

class Compiler():
  _library: Library 

  def __init__(self, constrains, optimization_constrains):
    self._constrains = self._list_to_constrains(constrains)
    self._optimization_constrains = self._list_to_constrains(optimization_constrains)

  def build(self) -> List[Part]:
    # TODO: Check if library exist and if library.keys > 0. If not raise an error
    sequence = []
    for constrain in self._constrains:
      part_solved = self._solve(constrain)
      if type(part_solved) != str:
        raise TypeError
      sequence.append(Part(constrain.name, part_solved))
    return sequence

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
