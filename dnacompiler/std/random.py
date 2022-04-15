import random
from enum import Enum
from dnacompiler.utils.Alphabet import Alphabet

RANDOM_GENERATOR = 'RANDOM_GENERATOR'

def genRandomSeqWithConstraints(seqLength,
                                alphabet,
                                forbiddenSeqs,
                                isNucleicAcid = True,
                                max_homopolymer_length = 4,
                                min_GC = 0.4,
                                max_GC = 0.6,
                                start_GC_count_at = 20, #this is the length at which GC counting kicks in
                                max_GC_stretch = 5,
                                max_AT_stretch = 5,
                                maxProblematicSteps = 1000,
                                maxAttemptedSteps = 10000):
    
    seq = ''
    iterator = 1
    totalSteps = 0
    numProblemSteps = 0
    
    #Generate forbidden homopolymers and append them to the forbiddenSeqs list
    for i in range(len(alphabet)):
      forbiddenHomopolymer = alphabet[i] * (max_homopolymer_length+1)
    #print forbiddenHomopolymer
      forbiddenSeqs.append(forbiddenHomopolymer)
    #print forbiddenSeqs
 
 
    while((iterator <= seqLength) & (totalSteps < maxAttemptedSteps)):
        #Each addition starts naive--noForbidden = True, until it's checked
        noForbidden = True
        
        seq = seq + random.choice(alphabet)
        #print seq
 
        currentSeqLen = len(seq)
        #print currentSeqLen
 
 
        #This loop looks for forbidden sequences in the string
        for i in forbiddenSeqs:
            #print (i in seq)
            if(i in seq): 
                    noForbidden = False
                    #print i
 
        #Now calculate the GC content, if the sequence is nucleic acid
        if(isNucleicAcid):
            #Calculate GC content
            gCount = float(seq.count('G'))
            cCount = float(seq.count('C'))
            GC_content = (gCount + cCount) / currentSeqLen
            #print GC_content
 
            #Only calculate GC content for parts longer than start_GC_count_at
            if(currentSeqLen > start_GC_count_at):
                if(GC_content < 0.4):
                    noForbidden = False
                if(GC_content > 0.6):
                    noForbidden = False
            
            #Make sure there aren't local regions of low sequence complexity (all AT or all GC)
            if(currentSeqLen > max_GC_stretch):
                lastNbp = seq[currentSeqLen-max_GC_stretch:currentSeqLen]
                #print lastNbp
                if(('A' not in lastNbp) & ('T' not in lastNbp) & ('U' not in lastNbp)):
                    noForbidden = False
            if(currentSeqLen > max_AT_stretch):
                lastNbp = seq[currentSeqLen-max_AT_stretch:currentSeqLen]
                if(('G' not in lastNbp) & ('C' not in lastNbp)):
                    noForbidden = False
            
 
        #print noForbidden
        #Of everything checks out, move on to the next letter in the sequence
        if(noForbidden):
            iterator = iterator + 1
        #Otherwise, delete 1-2 letters and try again
        else:
            numProblemSteps = numProblemSteps + 1
            #print numProblemSteps
            #If the sequence gets stuck on a problematic region for too long, just delete the whole sequence and start again
            if(numProblemSteps > maxProblematicSteps):
                print('stuck on this sequence! resetting.')
                print('seq before resetting: ' + seq)
                seq = ''
                iterator = 1
                numProblemSteps = 0
            else:
                if(currentSeqLen == 1):
                    seq = ''
                else:
                    if(currentSeqLen == 2):
                        seq = seq[0:currentSeqLen-1]
                    else:
                        if(currentSeqLen > 2):
                            seq = seq[0:currentSeqLen-2]
                            iterator = iterator - 1
    #                    else:
    #                        if(currentSeqLen > 3):
    #                            seq = seq[0:currentSeqLen-3]
    #                            iterator = iterator - 2
        #print iterator
        #print seq
        
        totalSteps = totalSteps+1
        #print count
    if(totalSteps >= maxAttemptedSteps):
        print('Something went wrong! Could not find an answer for ' + str(maxAttemptedSteps) + ' steps.')
        #print('Probably the GC content of the first 10 bp was skewed.')
        print('Maybe try again?')
    return seq

def random_sequence_generator(args):
  length = int(args.get('length'))
  alphabet = args.get('alphabet')
  forbidden = args.get('forbidden')
 
  if not alphabet in Alphabet.__members__:
    raise ValueError

  alphabet = Alphabet.__members__.get(alphabet).value

  if not isinstance(forbidden, list):
    forbidden = []

  return genRandomSeqWithConstraints(length, alphabet, forbidden)

random_collection = {
  RANDOM_GENERATOR: random_sequence_generator 
}

