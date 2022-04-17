from typing import List
from dnacompiler.Part import Part

class Sequence:
  features: List[Part] 
  sequence: str
  
  def __init__(self, features):
    self.features = features
    self.sequence = self._build_sequence(features)
  
  def _build_sequence(self, features):
    sequence = ""
    for feature in features:
      sequence += feature.value
    return sequence


