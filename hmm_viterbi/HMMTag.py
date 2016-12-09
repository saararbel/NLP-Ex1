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


if __name__ == '__main__':
    words_in_input_file = readFile(sys[1]).split()
    q_mle_lines = [line.split(' ') for line in readFile(sys[2]).split('\n')]
    e_mle = readFile(sys[3])
    out_file_name = readFile(sys[4])
    extra_file_name = readFile(sys[5])
