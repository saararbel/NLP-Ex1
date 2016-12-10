import sys

def readFile(filePath):
    with open(filePath) as inputFile:
        return inputFile.read()


def vitterbi_algorithm(words, e_mle, q_mle, tags):
    v = {}
    v[(0, 'start', 'start')] = 1

    for i, word in enumerate(words):
        for t in tags:
            for r in tags:
                max_vitterbi = 0
                max_t_tag = 0
                for t_tag in tags:
                    temp_v = v[(i - 1, t_tag, t)] * q_mle[(t_tag, t, r)] * e_mle[(r, word)]
                    if temp_v > max_vitterbi:
                        max_vitterbi = temp_v
                        max_t_tag = t_tag
                v[(i, t, r)] = max_t_tag

    return v


def extractTags(q_mle_lines):
    tags = set()
    for line in q_mle_lines:
        tags.add(line[0])
        tags.add(line[1])
        tags.add(line[2])

    return tags

def parseQmleFile(qMleFilePath):
    parsedFile = [line.split(' ') for line in readFile(qMleFilePath).split('\n')]
    qMle = {}
    for line in parsedFile:
        qMle[(line[0],line[1],line[2])] = [float(e) for e in line[3:]]

    return qMle


def parseEmleFile(eMleFilePath):
    parsedFile = [line.split(' ') for line in readFile(eMleFilePath).split('\n')]
    eMle = {}
    for line in parsedFile:
        eMle[(line[0],line[1])] = float(line[2])


if __name__ == '__main__':
    words_in_input_file = readFile(sys.argv[1]).split()
    q_mle_lines = parseQmleFile(sys.argv[2])
    e_mle = parseEmleFile(sys.argv[3])
    vitterbi_algorithm(words_in_input_file,e_mle,q_mle_lines, extractTags(q_mle_lines))

    # out_file_name = readFile(sys.argv[4])
    # extra_file_name = readFile(sys.argv[5])
