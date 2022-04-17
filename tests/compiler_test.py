import unittest
from dnacompiler.Compiler import Compiler
from dnacompiler.Library import Library
from dnacompiler.std.random import random_collection, RANDOM_GENERATOR
from dnacompiler.std.promoters import anderson_promoters, J23100
from dnacompiler.std.rbss import rbs_collection, B0034 
from dnacompiler.std.terminators import terminator_collection, B0015
from dnacompiler.utils.Conversion import sequences2gb

class TestCompiler(unittest.TestCase):

  def test_build_normal_constrain(self):
    library = Library()
    library.add('Random Sequence', 'ATCG')
    compiler = Compiler([{ 'constrain': 'Random Sequence'}], [])
    compiler.setLibrary(library)
    sequences = compiler.build()
    self.assertEqual(len(sequences), 1)
    self.assertEqual(len(sequences[0].features), 1)
    self.assertEqual(sequences[0].sequence, 'ATCG')

  def test_build_func_constrain(self):
    def x():
      return 'CGTA'
    library = Library()
    library.add('Random Sequence', x)
    compiler = Compiler([{ 'constrain': 'Random Sequence'}], [])
    compiler.setLibrary(library)
    sequences = compiler.build()
    self.assertEqual(len(sequences), 1)
    self.assertEqual(len(sequences[0].features), 1)
    self.assertEqual(sequences[0].sequence, 'CGTA')

  def test_build_func_constrain_with_args(self):
    def x(args: str):
      if args == None:
        raise ValueError
      return args[0]
    library = Library()
    library.add('Random Sequence', x)
    compiler = Compiler([{ 'constrain': 'Random Sequence', 'args': ['CCGA']}], [])
    compiler.setLibrary(library)
    sequences = compiler.build()
    self.assertEqual(len(sequences), 1)
    self.assertEqual(len(sequences[0].features), 1)
    self.assertEqual(sequences[0].sequence, 'CCGA')

  def test_combinatorial_constrains(self):
    primers_collection = {
      'PRIMERS': [
        {
          'name': 'PrimerA',
          'value': 'AAAA'
        },
        {
          'name': 'PrimerT',
          'value': 'TTTT'
        },
        {
          'name': 'PrimerC',
          'value': 'CCCC'
        },
      ]
    }
    library = Library([ random_collection, primers_collection ])
    constrains = [
      {
        'constrain': 'PRIMERS'
      },
      {
        'constrain': RANDOM_GENERATOR,
        'args': {
          'length': '12',
          'alphabet': 'DNA'
         }
      },
    ]
    compiler = Compiler(constrains)
    compiler.setLibrary(library)
    sequences = compiler.build()
    self.assertEqual(len(sequences), 3)
    for sequence in sequences:
      self.assertEqual(len(sequence.features), 2)
      self.assertEqual(len(sequence.features[0].value), 4)
      self.assertEqual(len(sequence.features[1].value), 12)

  
  def test_to_genbank(self):
    library = Library()
    library.add('Random Sequence', 'ATCG')
    compiler = Compiler([{ 'constrain': 'Random Sequence'}], [])
    compiler.setLibrary(library)
    sequences = compiler.build()
    sequences2gb(sequences)


  def test_whole_sequence(self):
    target_proteins = {
      'TARGET_PROTEINS': [
        {
          'name': 'RFP',
          'value': 'atggcttcctccgaagacgttatcaaagagttcatgcgtttcaaagttcgtatggaaggttccgttaacggtcacgagttcgaaatcgaaggtgaaggtgaaggtcgtccgtacgaaggtacccagaccgctaaactgaaagttaccaaaggtggtccgctgccgttcgcttgggacatcctgtccccgcagttccagtacggttccaaagcttacgttaaacacccggctgacatcccggactacctgaaactgtccttcccggaaggtttcaaatgggaacgtgttatgaacttcgaagacggtggtgttgttaccgttacccaggactcctccctgcaagacggtgagttcatctacaaagttaaactgcgtggtaccaacttcccgtccgacggtccggttatgcagaaaaaaaccatgggttgggaagcttccaccgaacgtatgtacccggaagacggtgctctgaaaggtgaaatcaaaatgcgtctgaaactgaaagacggtggtcactacgacgctgaagttaaaaccacctacatggctaaaaaaccggttcagctgccgggtgcttacaaaaccgacatcaaactggacatcacctcccacaacgaagactacaccatcgttgaacagtacgaacgtgctgaaggtcgtcactccaccggtgcttaataacgctgatagtgctagtgtagatcgc'
        },
        {
          'name': 'GFP',
          'value': 'atgcgtaaaggagaagaacttttcactggagttgtcccaattcttgttgaattagatggtgatgttaatgggcacaaattttctgtcagtggagagggtgaaggtgatgcaacatacggaaaacttacccttaaatttatttgcactactggaaaactacctgttccatggccaacacttgtcactactttcggttatggtgttcaatgctttgcgagatacccagatcatatgaaacagcatgactttttcaagagtgccatgcccgaaggttatgtacaggaaagaactatatttttcaaagatgacgggaactacaagacacgtgctgaagtcaagtttgaaggtgatacccttgttaatagaatcgagttaaaaggtattgattttaaagaagatggaaacattcttggacacaaattggaatacaactataactcacacaatgtatacatcatggcagacaaacaaaagaatggaatcaaagttaacttcaaaattagacacaacattgaagatggaagcgttcaactagcagaccattatcaacaaaatactccaattggcgatggccctgtccttttaccagacaaccattacctgtccacacaatctgccctttcgaaagatcccaacgaaaagagagaccacatggtccttcttgagtttgtaacagctgctgggattacacatggcatggatgaactatacaaataataa'
        },
      ]
    }

    library = Library([random_collection, anderson_promoters, rbs_collection, terminator_collection, target_proteins])

    requirements = [
      {
        'constrain': RANDOM_GENERATOR,
        'args': {
          'length': '12',
          'alphabet': 'DNA'
         }
      },
      {
        'constrain': J23100
      },
      {
        'constrain': B0034
      },
      {
        'constrain': 'TARGET_PROTEINS'
      },
      {
        'constrain': B0015
      },
      {
        'constrain': RANDOM_GENERATOR,
        'args': {
          'length': '12',
          'alphabet': 'DNA'
         }
      },
    ]
	
    compiler = Compiler(requirements)
    compiler.setLibrary(library)
    sequences = compiler.build()

    for sequence in sequences:
      for part in sequence.features:
        print(part.name, part.value)

  def test_whole_sequence_combinatorial(self):
    my_proteins = {
        'RFP': 'atggcttcctccgaagacgttatcaaagagttcatgcgtttcaaagttcgtatggaaggttccgttaacggtcacgagttcgaaatcgaaggtgaaggtgaaggtcgtccgtacgaaggtacccagaccgctaaactgaaagttaccaaaggtggtccgctgccgttcgcttgggacatcctgtccccgcagttccagtacggttccaaagcttacgttaaacacccggctgacatcccggactacctgaaactgtccttcccggaaggtttcaaatgggaacgtgttatgaacttcgaagacggtggtgttgttaccgttacccaggactcctccctgcaagacggtgagttcatctacaaagttaaactgcgtggtaccaacttcccgtccgacggtccggttatgcagaaaaaaaccatgggttgggaagcttccaccgaacgtatgtacccggaagacggtgctctgaaaggtgaaatcaaaatgcgtctgaaactgaaagacggtggtcactacgacgctgaagttaaaaccacctacatggctaaaaaaccggttcagctgccgggtgcttacaaaaccgacatcaaactggacatcacctcccacaacgaagactacaccatcgttgaacagtacgaacgtgctgaaggtcgtcactccaccggtgcttaataacgctgatagtgctagtgtagatcgc',
        'GFP': 'atgcgtaaaggagaagaacttttcactggagttgtcccaattcttgttgaattagatggtgatgttaatgggcacaaattttctgtcagtggagagggtgaaggtgatgcaacatacggaaaacttacccttaaatttatttgcactactggaaaactacctgttccatggccaacacttgtcactactttcggttatggtgttcaatgctttgcgagatacccagatcatatgaaacagcatgactttttcaagagtgccatgcccgaaggttatgtacaggaaagaactatatttttcaaagatgacgggaactacaagacacgtgctgaagtcaagtttgaaggtgatacccttgttaatagaatcgagttaaaaggtattgattttaaagaagatggaaacattcttggacacaaattggaatacaactataactcacacaatgtatacatcatggcagacaaacaaaagaatggaatcaaagttaacttcaaaattagacacaacattgaagatggaagcgttcaactagcagaccattatcaacaaaatactccaattggcgatggccctgtccttttaccagacaaccattacctgtccacacaatctgccctttcgaaagatcccaacgaaaagagagaccacatggtccttcttgagtttgtaacagctgctgggattacacatggcatggatgaactatacaaataataa'
    }

    library = Library([random_collection, anderson_promoters, rbs_collection, terminator_collection, my_proteins])

    requirements = [
      {
        'constrain': RANDOM_GENERATOR,
        'args': {
          'length': '12',
          'alphabet': 'DNA'
         }
      },
      {
        'constrain': J23100
      },
      {
        'constrain': B0034
      },
      {
        'constrain': 'RFP'
      },
      {
        'constrain': B0015
      },
      {
        'constrain': RANDOM_GENERATOR,
        'args': {
          'length': '12',
          'alphabet': 'DNA'
         }
      },
    ]
	
    compiler = Compiler(requirements)
    compiler.setLibrary(library)
    sequences = compiler.build()

    for sequence in sequences:
      for part in sequence.features:
        print(part.name, part.value)

    

if __name__ == "__main__":
  unittest.main()
