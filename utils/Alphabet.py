from enum import Enum

class Alphabet(Enum):
  DNA = 'AGCT'
  RNA = 'AGCU'
  Protein = 'ACDEFGHIKLMNPQRSTVWY*'
  Protein_noStop = 'ACDEFGHIKLMNPQRSTVWY'
  Protein_Polar = 'DEGHKNQRST'
  Protein_Charged = 'DEKR'
  Protein_Cationic = 'HKR'
  Protein_Cationic_noHis = 'KR'
  Protein_Anionic = 'DE'
  Protein_Small = 'AGST'
  Protein_SmallAndHydrophilic = 'GST'
  Protein_OnlyHydrophobic = 'ACFILMPVWY'
  Protein_OnlyHydrophobic_noCysteine = 'AFILMPVWY'
