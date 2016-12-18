import os
import sys
from cStringIO import StringIO
from collections import Counter

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from memm import general_features
from memm.general_features import GeneralFeatures
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
    print "History built"
    return histories


def feature_builders(not_rare_words, word):
    if word in not_rare_words:
        return NotRareFeatures.FEATURES

    return RareFeatures.FEATURES


def extract_features_from_histories(histories, not_rare_words):
    features = []
    for history in histories:
        for feature_builder in feature_builders(not_rare_words, history['wi']):
            features.append(feature_builder.from_history(history))
            # print "Finished features for " + history['wi'] + ", " + history['ti']
    print "features extracted"
    return features


def to_feature_lines(histories, unique_features, tags, output_file_path='features_output.txt'):
    tags_indexes = dict((tag, index) for index, tag in enumerate(tags))
    enumerated_unique_features = list(enumerate(unique_features))
    # with open(output_file_path, 'w') as output_file:
    with open(output_file_path, 'w') as output_file:
        print 'File "%s" tuncated' % output_file_path
    file_str = StringIO()
    for word_index, history in enumerate(histories):
        file_str.write("%s " % tags_indexes[history['ti']])
        file_str.write(':1 '.join([str(i) for i, feature in enumerated_unique_features if feature.test(history)]))
        file_str.write(':1\n')
        if word_index % 100 == 0:
            print "Word %s checked" % word_index
            if word_index % 10000 == 0:
                with open(output_file_path, 'a') as output_file:
                    output_file.write(file_str.getvalue())
                    file_str = StringIO()
    with open(output_file_path, 'a') as output_file:
        output_file.write(file_str.getvalue())


if __name__ == '__main__':
    raw_seq_lines = parse_input_file(sys.argv[1])
    tagged_lines, non_rare_words, tags = extract_data(raw_seq_lines)
    print 'Tags: [' + '|'.join(tag + ' ' + str(i) for i, tag in enumerate(tags)) + ']'
    print 'Words, total %s ' % sum(len(x) for x in tagged_lines)
    histories = build_history(tagged_lines, non_rare_words)
    features = extract_features_from_histories(histories, non_rare_words)

    unique_features = set(features)
    print "Finished features: %s, unique: %s" % (str(len(features)), str(len(unique_features)))

    to_feature_lines(histories, unique_features, tags)
    print "Finished writing to output file"
