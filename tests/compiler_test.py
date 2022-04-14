import unittest
from dnacompiler.Compiler import Compiler
from dnacompiler.Library import Library

class TestCompiler(unittest.TestCase):

  def test_build_normal_constrain(self):
    library = Library()
    library.add('Random Sequence', 'ATCG')
    compiler = Compiler([{ 'constrain': 'Random Sequence'}], [])
    compiler.setLibrary(library)
    sequence = compiler.build()
    self.assertEqual(len(sequence), 1)
    self.assertEqual(sequence[0].sequence, 'ATCG')

  def test_build_func_constrain(self):
    def x():
      return 'CGTA'
    library = Library()
    library.add('Random Sequence', x)
    compiler = Compiler([{ 'constrain': 'Random Sequence'}], [])
    compiler.setLibrary(library)
    sequence = compiler.build()
    self.assertEqual(len(sequence), 1)
    self.assertEqual(sequence[0].sequence, 'CGTA')

  def test_build_func_constrain_with_args(self):
    def x(args: str):
      if args == None:
        raise ValueError
      return args[0]
    library = Library()
    library.add('Random Sequence', x)
    compiler = Compiler([{ 'constrain': 'Random Sequence', 'args': ['CCGA']}], [])
    compiler.setLibrary(library)
    sequence = compiler.build()
    self.assertEqual(len(sequence), 1)
    self.assertEqual(sequence[0].sequence, 'CCGA')

if __name__ == "__main__":
  unittest.main()
