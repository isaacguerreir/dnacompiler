class Part:
    def __init__(self, name: str, value, partType = None):
      self.name = name
      self.value = value
      self.partType = partType
    
    def setPosition(self, pos: int):
      self.pos = pos
