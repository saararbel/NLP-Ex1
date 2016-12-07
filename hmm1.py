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


if __name__ == '__main__':
    parsedFile = parseInputFile()
    words,tags, wordsAndTags = buildLists()

    calcQprob(tags, len(set(words)))

    # eFile = open(sys.argv[2],'w')
    # eMle = calcEprob(words,tags,wordsAndTags)
    # for (word,tag) in eMle :
    #     eFile.write(word+","+tag + " = " + str(eMle[(word,tag)]) + "\n")






