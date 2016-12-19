import os
import shelve
import sys
from contextlib import closing
from math import log

# sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from liblin import LiblinearLogregPredictor
from hmm_viterbi.HMMTag import extract_words
from memm.non_rare_features import NotRareFeatures
from memm.rare_features import RareFeatures

ALL_FEATURES = NotRareFeatures.FEATURES + RareFeatures.ONLY_RARE


def extract_features_indexes_from(history, features):
    active_features = []
    for feature_builder in ALL_FEATURES:
        for feature in feature_builder.multiple_from_history(history):
            if feature in features:
                active_features.append(int(features[feature]))
    return active_features


def vitterbi_algorithm(lines, llp, features, tags):
    final_line_tags = []
    for line_number, line in enumerate(lines):
        v = [{('start', 'start'): 0}]
        bp = []
        for i, word in enumerate(line):
            maxProb = {}
            max_prob_tag = {}
            for t_tag, t in v[i]:
                history = build_history(i, line, t, t_tag, word)
                tags_with_prob = llp.predict(extract_features_indexes_from(history, features))
                for r_tag, r_prob in tags_with_prob.iteritems():
                    r_prob = v[i][(t_tag, t)] + log(r_prob)
                    r_real_tag = tags[int(r_tag)]
                    if (t, r_real_tag) not in maxProb or r_prob > maxProb[(t, r_real_tag)]:
                        maxProb[(t, r_real_tag)] = r_prob
                        max_prob_tag[(t, r_real_tag)] = t_tag
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
        print final_line_tags[-1]

    return final_line_tags


def build_history(i, line, t, t_tag, word):
    return {'wi': word, 'wi-1': line[i - 1] if i > 0 else 'start',
            'wi-2': line[i - 2] if i > 1 else 'start',
            'wi+1': line[i + 1] if i < len(line) - 1 else 'end',
            'wi+2': line[i + 2] if i < len(line) - 2 else 'end', 'ti-1': t,
            'ti-2': t_tag}


if __name__ == '__main__':
    input_file_name = sys.argv[1]
    modelname = sys.argv[2]
    out_file_name = sys.argv[3]
    other_file_name = sys.argv[4]
    llp = LiblinearLogregPredictor(modelname)
    lines = extract_words(input_file_name)
    with closing(shelve.open(other_file_name)) as shelf:
        tagged_lines = vitterbi_algorithm(lines, llp, shelf['features'], shelf['tags'])
        with open(out_file_name, 'w') as out_file:
            out_file.write('\n'.join(' '.join(tagged_line) for tagged_line in tagged_lines) + '\n')
