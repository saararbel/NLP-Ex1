import sys
from MLETrain import calc_e_prob
from MLETrain import calcQprob


def parseInputFile():
    trainFilePath = sys.argv[1]
    with open(trainFilePath) as inputFile:
        return inputFile.read().split('\n')


def buildLists(parsedFile):
    words = []
    tags = []
    wordsAndTags = []
    for line in parsedFile[:-1]:
        lst = []
        lst.append('start')
        lst.append('start')
        for seq in line.split(' '):
            splitted = seq.rsplit('/', 1)
            words.append(splitted[0])
            lst.append(splitted[1])
            wordsAndTags.append((splitted[0], splitted[1]))
        tags.append(lst)

    return words, tags, wordsAndTags


def prepare_e(e_mle):
    return '\n'.join([' '.join([word, tag, str(e_mle[(word, tag)])]) for word, tag in e_mle])


def write_e_mle_file(words, tags, wordsAndTags):
    e_mle = calc_e_prob(words, tags, wordsAndTags)
    open(sys.argv[2], 'w').write(prepare_e(e_mle))


def prepare_q(qprob):
    return '\n'.join([' '.join([w1, w2, w3] + [str(p) for p in qprob[(w1, w2, w3)]]) for w1, w2, w3 in qprob])


def write_q_mle_file():
    open(sys.argv[3], 'w').write(prepare_q(qprob))


if __name__ == '__main__':
    parsedFile = parseInputFile()
    words, tags, wordsAndTags = buildLists(parsedFile)
    print "words and tags extracted"

    qprob = calcQprob(tags, len(words))
    write_q_mle_file()
    print "q calculated"

    write_e_mle_file(words, tags, wordsAndTags)
    print "Finished"
