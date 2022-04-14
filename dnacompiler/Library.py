from types import FunctionType

class Library:

  def __init__(self, collection = None):
    self._library = dict() 
    if collection != None:
      self.import_collection(collection)

  def add(self, key, value):
    typeOf = type(value)
    if typeOf == str or typeOf == FunctionType or isinstance(value, list):
      self._library[key] = value
    else:
      raise TypeError

  def get(self, key):
    return self._library[key]

  def import_collection(self, collection):
    if isinstance(collection, list):
      for obj in collection:
        self._import_obj(obj)
      return
    if isinstance(collection, dict):
      self._import_obj(collection)
      return
    raise ValueError

  def _import_obj(self, obj):
    for key, value in obj.items():
      self.add(key, value)

  def __len__(self):
    return len(self._library)
