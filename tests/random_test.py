import unittest
from std.random import random_collection 
from dnacompiler.Library import Library
from dnacompiler.Compiler import Compiler

class TestRandom(unittest.TestCase):
  def test_random_dna(self):
    library = Library(random_collection)
    compiler = Compiler([
      {
        'constrain': 'RANDOM_GENERATOR',
        'args': {
          'length': '12',
          'alphabet': 'DNA'
         }
      }
    ])
    compiler.setLibrary(library)
    sequences = compiler.build()
    self.assertEqual(len(sequences), 1)
    self.assertEqual(len(sequences[0]), 1)
    self.assertEqual(len(sequences[0][0].value), 12)

if __name__ == "__main__":
  unittest.main()
