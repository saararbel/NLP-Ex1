import sys


def readFile(filePath):
    with open(filePath) as inputFile:
        return inputFile.read()


def vitterbi_algorithm(words, e_mle, q_mle, tags):
    v = {(0, 'start', 'start'): 1}

    for i, word in enumerate(words):
        for t in tags:
            for r in tags:
                max_vitterbi = 0
                for t_tag in tags:
                    temp_v = v[(i, t_tag, t)] * q_mle[(t_tag, t, r)] * e_mle[(word, r)]
                    if temp_v > max_vitterbi:
                        max_vitterbi = temp_v
                v[(i + 1, t, r)] = max_vitterbi

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
