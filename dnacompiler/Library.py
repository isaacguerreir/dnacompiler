import types

class Library:
  _library = dict() 
   
  def add(self, key, value):
    typeOf = type(value)
    if typeOf == str or typeOf == types.FunctionType:
      self._library[key] = value
    else:
      raise TypeError

  def get_value(self, key):
    return self._library[key]
