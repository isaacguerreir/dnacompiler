class Part:
    def __init__(self, name: str, sequence: str, sequenceType = None):
      self.name = name
      self.sequence = sequence
      self.sequenceType = sequenceType
    
    def setPosition(self, pos: int):
      self.pos = pos
