import unittest
from dnacompiler.Library import Library

class TestLibrary(unittest.TestCase):
  def test_add_raise_type_error(self):
    library = Library()

    for value in [1, 1.0, {}]:
      with self.assertRaises(TypeError):
        library.add('key', value)

  def test_add(self):
    library = Library()
    
    def fun():
      pass

    for value in ['str', fun]:
      library.add('key', value)
      self.assertEqual(library.get('key'), value)

  def test_import_collection(self):
    library = Library()

    collection = [{
        'DNA A': 'ATCGCGCG'
      },
      {
        'DNA B': 'AAAAAA'
    }]

    dict_collection = {
      'DNA C': 'CCCCCCCCCC',
      'DNA D': 'GGGGGGGGGG'
    }
    
    self.assertEqual(len(library), 0)
    library.import_collection(collection)
    self.assertEqual(len(library), 2)
    library.import_collection(dict_collection)
    self.assertEqual(len(library), 4)

if __name__ == "__main__":
  unittest.main()
