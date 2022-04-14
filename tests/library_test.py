import unittest
from dnacompiler.Library import Library

class TestLibrary(unittest.TestCase):
  def test_add_raise_type_error(self):
    library = Library()

    for value in [1, 1.0, [], {}]:
      with self.assertRaises(TypeError):
        library.add('key', value)

  def test_add(self):
    library = Library()
    
    def fun():
      pass

    for value in ['str', fun]:
      library.add('key', value)
      self.assertEqual(library.get('key'), value)


if __name__ == "__main__":
  unittest.main()
