import unittest
from dnacompiler.std.random import random_collection, RANDOM_GENERATOR 
from dnacompiler.Library import Library
from dnacompiler.Compiler import Compiler

class TestRandom(unittest.TestCase):
  def test_random_dna(self):
    library = Library(random_collection)
    compiler = Compiler([
      {
        'constrain': RANDOM_GENERATOR,
        'args': {
          'length': '12',
          'alphabet': 'DNA'
         }
      }
    ])
    compiler.setLibrary(library)
    sequences = compiler.build()
    self.assertEqual(len(sequences), 1)
    self.assertEqual(len(sequences[0].features), 1)
    self.assertEqual(len(sequences[0].sequence), 12)

if __name__ == "__main__":
  unittest.main()
