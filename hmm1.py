import sys
from MleCalculator import calcEprob
from MleCalculator import  calcQprob


def parseInputFile():
    trainFilePath = sys.argv[1]
    with open(trainFilePath) as inputFile:
        return inputFile.read().split()


def buildLists():
    words=[]
    tags=[]
    wordsAndTags=[]
    for seq in parsedFile:
        splitted = seq.rsplit('/',1)
        words.append(splitted[0])
        tags.append(splitted[1])
        wordsAndTags.append((splitted[0], splitted[1]))

    return words,tags,wordsAndTags


def writeEmleFile():
    eFile = open(sys.argv[2], 'w')
    eMle = calcEprob(words, tags, wordsAndTags)
    for (word, tag) in eMle:
        eFile.write(word + "," + tag + " = " + str(eMle[(word, tag)]) + "\n")


def prepare_for_writing(qprob):
    return '\n'.join([' '.join([w1, w2, w3] + [str(p) for p in qprob[(w1, w2, w3)]]) for w1, w2, w3 in qprob])


if __name__ == '__main__':
    parsedFile = parseInputFile()
    words,tags, wordsAndTags = buildLists()

    qprob = calcQprob(tags, len(set(words)))
    open(sys.argv[3], 'w').write(prepare_for_writing(qprob))
    



    writeEmleFile()








