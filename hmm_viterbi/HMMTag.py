import sys

def readFile(filePath):
    with open(filePath) as inputFile:
        return inputFile.read()


def backoff(probs):
    return (float(probs[0]) + float(probs[1]) + float(probs[2])) / 3


def sintisize(e_mle, param):
    if param not in e_mle:
        return 0.0

    return e_mle[param]


def vitterbi_algorithm(words, e_mle, q_mle, tags):
    v = {}
    bp = {}

    v[(0, 'start', 'start')] = 1

    # first iteration
    for tag1 in tags:
        v[(1,'start',tag1)] = q_mle[('start','start',tag1)] * e_mle[(tag1, words[0])]
        bp[(1,tag1)] = 'start'

    # second iteration
    for tag1 in tags:
        for tag2 in tags:
            v[(2,tag1,tag2)] = v[(1,bp[(1,tag1)],tag1)] * q_mle[(bp[(1,tag1)],tag1,tag2)] * e_mle[(tag2, words[1])]

        bp[(2, tag2)] = tag1

    # third iteration
    for tag1 in tags:
        for tag2 in tags:
            v[(3,tag1,tag2)] = v[(2,bp[(2,tag1)] ,tag1)] * q_mle[(bp[(2,tag1)],tag1,tag2)] * e_mle[(tag2, words[2])]




    for i, word in enumerate(words):
        for t in tags:
            for r in tags:
                v[(i+1, )]

    return v


def extractTags(q_mle_lines):
    tags = set()
    for line in q_mle_lines:
        tags.update(line[:3])

    return tags


def parse_q_mle_file(q_mle_file_path):
    parsed_file = [line.split(' ') for line in readFile(q_mle_file_path).split('\n')]
    q_mle = {}
    for line in parsed_file:
        q_mle[(line[0], line[1], line[2])] = [float(e) for e in line[3:]]

    return q_mle


def parse_e_mle_file(e_mle_file_path):
    parsed_file = [line.split(' ') for line in readFile(e_mle_file_path).split('\n')]
    e_mle = {}
    for line in parsed_file:
        e_mle[(line[0], line[1])] = float(line[2])

    return e_mle


if __name__ == '__main__':
    words_in_input_file = readFile(sys.argv[1]).split()
    q_mle_lines = parse_q_mle_file(sys.argv[2])
    e_mle = parse_e_mle_file(sys.argv[3])
    vitterbi_algorithm(words_in_input_file, e_mle, q_mle_lines, extractTags(q_mle_lines))

    # out_file_name = readFile(sys.argv[4])
    # extra_file_name = readFile(sys.argv[5])
