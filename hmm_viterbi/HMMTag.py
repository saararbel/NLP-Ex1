import sys
from math import log


def readFile(filePath):
    with open(filePath) as inputFile:
        return inputFile.readlines()


def backoff(probs):
    lambda1 = 0.8
    lambda2 = 0.1
    return lambda1 * float(probs[0]) + lambda2 * float(probs[1]) + (1.0 - lambda2 - lambda1) * float(probs[2])


def sintisize(e_mle, param):
    if param not in e_mle:
        return e_mle[('very_very_rare_word_5_5_5', param[1])]

    return e_mle[param]


def vitterbi_algorithm(lines, e_mle, q_mle, tags):
    final_line_tags = []
    for line_number, line in enumerate(lines):
        v = [{('start', 'start'): 0}]
        bp = []
        for i, word in enumerate(line):
            maxProb = {}
            max_prob_tag = {}
            for t_tag, t in v[i]:
                for r in tags:
                    e = sintisize(e_mle, (word, r))
                    if e != 0.0:
                        temp = v[i][(t_tag, t)] + log(backoff(q_mle[(t_tag, t, r)])) + log(e)
                        if (t, r) not in maxProb or temp > maxProb[(t, r)]:
                            maxProb[(t, r)] = temp
                            max_prob_tag[(t, r)] = t_tag
            v.append(maxProb)
            bp.append(max_prob_tag)
        print line_number
        before_last_tag, last_tag = max(v[-1], key=lambda tuple: tuple[-1])
        line_tags = [last_tag]
        if before_last_tag != 'start':
            line_tags.append(before_last_tag)
        for j in xrange(len(v) - 2, 1, -1):
            prev_t = bp[j][(before_last_tag, last_tag)]
            line_tags.append(prev_t)
            last_tag = before_last_tag
            before_last_tag = prev_t
        final_line_tags.append(list(reversed(line_tags)))

    return final_line_tags


def extractTags(q_mle_lines):
    tags = set()
    for line in q_mle_lines:
        tags.update(line[:3])

    return tags


def parse_q_mle_file(q_mle_file_path):
    parsed_file = extract_words(q_mle_file_path)
    q_mle = {}
    for line in parsed_file:
        q_mle[(line[0], line[1], line[2])] = [float(e) for e in line[3:]]

    return q_mle


def parse_e_mle_file(e_mle_file_path):
    parsed_file = extract_words(e_mle_file_path)
    e_mle = {}
    for line in parsed_file:
        e_mle[(line[0], line[1])] = float(line[2])

    return e_mle


def extract_words(file_name):
    return [line[:-1].split(' ') for line in readFile(file_name)]


def real_tag_lines(args):
    pass


def calulate_acurracy(tag_lines, real_tag_lines):
    total = 0
    correct = 0

    for i, line in enumerate(tag_lines):
        for j, tag in enumerate(line):
            total += 1
            print "i, j = " + str(i) + ", " + str(j)
            if tag == real_tag_lines[i][j]:
                correct += 1

    return float(correct) / total


def extract_tags_from(test_file):
    return [blab(line) for line in extract_words(test_file)]


def blab(line):
    return [word_tag.rsplit('/', 1)[-1] for word_tag in line]


def as_tagged_dataset(sentences_in_input_file, tag_lines):
    output = ''

    for i, line in enumerate(sentences_in_input_file):
        for j, word in enumerate(line):
            output += word + '/' + tag_lines[i][j] + ' '
        output += '\n'

    return output


if __name__ == '__main__':
    sentences_in_input_file = extract_words(sys.argv[1])
    q_mle_lines = parse_q_mle_file(sys.argv[2])
    e_mle = parse_e_mle_file(sys.argv[3])
    tag_lines = vitterbi_algorithm(sentences_in_input_file, e_mle, q_mle_lines, extractTags(q_mle_lines))
    # real_tag_lines = extract_tags_from(sys.argv[4])
    # acurracy = calulate_acurracy(tag_lines, real_tag_lines)
    # print "acurracy: " + str(acurracy)
    open(sys.argv[4], 'w').write(as_tagged_dataset(sentences_in_input_file, tag_lines))
