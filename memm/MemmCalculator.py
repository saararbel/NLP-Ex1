import sys
from collections import Counter

def parseInputFile(trainFilePath):
    with open(trainFilePath) as inputFile:
        return inputFile.read().split('\n')


def buildLinesAndNotRareWords(trainingFile):
    lines = []
    words = []
    for line in trainingFile[:-1]:
        line_words_and_tags = []
        for seq in line.split(' '):
            splitted = seq.rsplit('/')
            line_words_and_tags.append((splitted[0],splitted[1]))
            words.append(splitted[0])
        lines.append(line_words_and_tags)

    words_counter = Counter(words)

    return lines, set([word for word,appear in words_counter.iteritems() if appear<5])

def getNotRareWords(trainingFile):
    words = []
    for line in trainingFile[:-1]:
        for seq in line.split(' '):
            splitted = seq.split('/')
            words.append(splitted[0])

    words_counter = Counter(words)
    return set([word for word,appear in words_counter.iteritems() if appear<5])

def calc_features(lines, not_rare_words):
    for line in lines:
        for (word,tag) in line:
            word_vector = []
            if word in not_rare_words:
                



if __name__ == '__main__':
    trainingFile = parseInputFile(sys.argv[1])
    lines,not_rare_words = buildLinesAndNotRareWords(trainingFile)
