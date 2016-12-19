import os
import shelve
import sys
from cStringIO import StringIO
from collections import Counter
from contextlib import closing

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from memm.non_rare_features import NotRareFeatures
from memm.rare_features import RareFeatures


def parse_input_file(trainFilePath):
    with open(trainFilePath) as inputFile:
        return inputFile.read().split('\n')


def extract_word_and_tag(seq):
    splitted = seq.rsplit('/', 1)

    return splitted[0], splitted[1]


def extract_data(trainingFile):
    tagged_lines = []
    words_counter = Counter()
    tags = set()
    for line in trainingFile[:-1]:
        tagged_words = []
        for seq in line.split(' '):
            word, tag = extract_word_and_tag(seq)
            tagged_words.append((word, tag))
            tags.add(tag)
            words_counter[word] += 1
        tagged_lines.append(tagged_words)

    return tagged_lines, set(word for word, ocurrences in words_counter.iteritems() if ocurrences > 5), sorted(
        list(tags))


def build_history(lines, not_rare_words):
    histories = []
    for line in lines:
        padded_line = [('start', 'start'), ('start', 'start')] + line + [('end', 'end'), ('end', 'end')]
        for i, word_tag_tuple in enumerate(line, 2):
            history = {'wi': word_tag_tuple[0], 'wi-1': padded_line[i - 1][0], 'wi-2': padded_line[i - 2][0],
                       'wi+1': padded_line[i + 1][0],
                       'wi+2': padded_line[i + 2][0], 'ti': word_tag_tuple[1], 'ti-1': padded_line[i - 1][1],
                       'ti-2': padded_line[i - 2][1]}
            histories.append(history)
    return histories


def feature_builders(not_rare_words, word):
    if word in not_rare_words:
        return NotRareFeatures.FEATURES

    return RareFeatures.FEATURES


def to_feature_lines(histories, not_rare_words, indexed_tags):
    index = 1
    features = {}
    features_file = StringIO()
    for history in histories:
        word_features = []
        for feature_builder in feature_builders(not_rare_words, history['wi']):
            for feature in feature_builder.multiple_from_history(history):
                if feature not in features:
                    features[feature] = index
                    index += 1
                word_features.append(features[feature])
        features_file.write("%s " % indexed_tags[history['ti']])
        features_file.write(':1 '.join(str(i) for i in sorted(word_features)))
        features_file.write(':1\n')

    return features_file.getvalue(), features


def write_output_file(output, output_file_path):
    with open(output_file_path, 'w') as output_file:
        output_file.write(output)


def index_tags(tags):
    return dict((tag, str(index)) for index, tag in enumerate(tags))


def stringify_tag(tag, index):
    return '%s %s' % (tag, index)


def marshal_tags_and_features(tags_and_features_file, tags, features):
    with closing(shelve.open(tags_and_features_file)) as shelf:
        shelf['tags'] = tags
        shelf['features'] = features
    print "Wrote tags and features to shelf file: %s" % tags_and_features_file


if __name__ == '__main__':
    raw_seq_lines = parse_input_file(sys.argv[1])
    tagged_lines, non_rare_words, tags = extract_data(raw_seq_lines)
    print 'Tags: [%s]' % '|'.join(stringify_tag(tag, i) for i, tag in enumerate(tags))
    # write_output_file(' '.join(tag for tag in tags), 'tags')
    print 'Words: total %s ' % sum(len(x) for x in tagged_lines)
    histories = build_history(tagged_lines, non_rare_words)
    print "History built"
    output, features = to_feature_lines(histories, non_rare_words, index_tags(tags))
    print 'total features: %s' % len(features)
    marshal_tags_and_features(sys.argv[3] if len(sys.argv) >= 4 else 'tags_and_features', tags, features)
    write_output_file(output, sys.argv[2] if len(sys.argv) >= 3 else 'features_output.txt')
