import sys


def readFile(filePath):
    with open(filePath) as inputFile:
        return inputFile.readlines()


def backoff(probs):
    return (float(probs[0]) + float(probs[1]) + float(probs[2])) / 3


def sintisize(e_mle, param):
    if param not in e_mle:
        return 0.0

    return e_mle[param]


def vitterbi_algorithm(lines, e_mle, q_mle, tags):
    vitt = []

    for words in lines:
        v = {(0, 'start', 'start'): 1}
        bp = {}
        for i, word in enumerate(words):
            for t in tags:
                for r in tags:
                    max_vitterbi = 0
                    max_t = None
                    for t_tag in tags:
                        if (i, t_tag, t) not in v:
                            v[(i, t_tag, t)] = 0
                        temp_v = v[(i, t_tag, t)] * backoff(q_mle[(t_tag, t, r)]) * sintisize(e_mle, (word, r))
                        if temp_v > max_vitterbi:
                            max_vitterbi = temp_v
                            max_t = t_tag
                    v[(i + 1, t, r)] = max_vitterbi
                    bp[(i, t, r)] = max_t
        vitt.append()
    #     TODO: continue viterbi


    return vitt


def extractTags(q_mle_lines):
    tags = set()
    for line in q_mle_lines:
        tags.update(line[:3])

    return tags


def parse_q_mle_file(q_mle_file_path):
    parsed_file = [line.split(' ') for line in readFile(q_mle_file_path)]
    q_mle = {}
    for line in parsed_file:
        q_mle[(line[0], line[1], line[2])] = [float(e) for e in line[3:]]

    return q_mle


def parse_e_mle_file(e_mle_file_path):
    parsed_file = [line.split(' ') for line in readFile(e_mle_file_path)]
    e_mle = {}
    for line in parsed_file:
        e_mle[(line[0], line[1])] = float(line[2])

    return e_mle


if __name__ == '__main__':
    sentences_in_input_file = [line.split(' ') for line in readFile(sys.argv[1])]
    q_mle_lines = parse_q_mle_file(sys.argv[2])
    e_mle = parse_e_mle_file(sys.argv[3])
    vitterbi_algorithm(sentences_in_input_file, e_mle, q_mle_lines, extractTags(q_mle_lines))

    # out_file_name = readFile(sys.argv[4])
    # extra_file_name = readFile(sys.argv[5])
