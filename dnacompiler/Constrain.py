from typing import Optional

class Constrain:
  name: str
  args: Optional[str]

  def __init__(self, name, args):
    self.name = name  
    self.args = args
