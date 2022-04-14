
import unittest
from dnacompiler.Compiler import Compiler

class TestCompiler(unittest.TestCase):

  def test_solve(self):
    compiler = Compiler([{ 'constrain': 'Random Sequence'}], [])
    self.assertEqual(compiler.solve(), True)

if __name__ == "__main__":
  unittest.main()
