import shelve
import sys
from contextlib import closing
from math import log

from hmm2.HMMTag import extract_words, extract_tags_from, calulate_acurracy
from liblin import LiblinearLogregPredictor
from memm1.non_rare_features import NotRareFeatures
from memm1.rare_features import RareFeatures

ALL_FEATURES = NotRareFeatures.FEATURES + RareFeatures.ONLY_RARE


def extract_features_indexes_from(history, features):
    active_features = []
    for feature_builder in ALL_FEATURES:
        for feature in feature_builder.multiple_from_history(history):
            if feature in features:
                active_features.append(int(features[feature]))
    return active_features


def get_max_tuple(v):
    max_prob = v.itervalues().next()
    max_key = None
    for key in v:
        if v[key] >= max_prob:
            max_prob = v[key]
            max_key = key
    return max_key


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
                feature_indexes = extract_features_indexes_from(history, features)
                tags_with_prob = llp.predict(feature_indexes)
                for r in tags_with_prob:
                    temp = v[i][(t_tag, t)] + log(tags_with_prob[r])
                    r_real_tag = tags[int(r)]
                    if (t, r_real_tag) not in maxProb or temp > maxProb[(t, r_real_tag)]:
                        maxProb[(t, r_real_tag)] = temp
                        max_prob_tag[(t, r_real_tag)] = t_tag
            v.append(maxProb)
            bp.append(max_prob_tag)
        print line_number
        # before_last_tag, last_tag = max(v[-1], key=lambda tuple: tuple[-1])
        before_last_tag, last_tag = get_max_tuple(v[-1])
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
        real_tag_lines = extract_tags_from('..\\ass1-tagger-test')
        accuracy = calulate_acurracy(tagged_lines, real_tag_lines)
        print "Accuracy: %s" % accuracy
        with open(out_file_name, 'w') as out_file:
            out_file.write('\n'.join(' '.join(tagged_line) for tagged_line in tagged_lines) + '\n')
