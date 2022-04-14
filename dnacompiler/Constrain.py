from typing import Optional

class Constrain:
  _name: str
  _args: Optional[str]

  def __init__(self, name, args):
    self._name = name  
    self._args = args
