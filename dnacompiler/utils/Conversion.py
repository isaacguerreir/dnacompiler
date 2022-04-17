from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
from dnacompiler.Sequence import Sequence
from dnacompiler.Part import Part
from typing import List
import time
import uuid

def sequences2gb(sequences: List[Sequence]):
  for sequence in sequences:
    id = str(uuid.uuid4())
    record = SeqRecord(
      Seq(sequence.sequence),
      id=id,
      annotations={"molecule_type": "dna"}
    )
    SeqIO.write(record, "{}.genbank".format(id), "genbank")

    

def getFeatures(sequence: Sequence):
  features = []
  start = 0
  for feature in sequence.features:
    end = start + len(feature.value)
    features.append(SeqFeature(FeatureLocation(start, end), type=feature.name))
    start = end + 1

  return features
  
