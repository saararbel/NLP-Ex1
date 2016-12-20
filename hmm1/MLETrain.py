from collections import Counter


def calc_e_prob(words, tag_lines, word_and_tags):
    counter = Counter(words)
    single_words = set([word for word, appear in counter.iteritems() if appear == 1])

    for idx,(word,tag) in enumerate(word_and_tags):
        if word in single_words:
            word_and_tags[idx] = ('very_very_rare_word_5_5_5',tag)

    for idx,word in enumerate(words):
        if word in single_words:
            words[idx] = 'very_very_rare_word_5_5_5'


    eMle = {}
    tagsSet = set()
    tagsCounter = Counter()
    for tags in tag_lines:
        tagsSet = tagsSet.union(tags)
        tagsCounter.update(tags)
    wordAndTagsCounter = Counter(word_and_tags)

    for word in set(words):
        for tag in tagsSet:
            eMle[(word, tag)] = float(wordAndTagsCounter[(word, tag)]) / tagsCounter[tag]

    return eMle


def calcQprob(tag_lines, numWords):
    qMle = {}
    tripletCounter = Counter()
    pairsCounter = Counter()
    onesCounter = Counter()
    tagSet = set()
    for tags in tag_lines:
        tripletsTags = zip(tags[:-2], tags[1:-1], tags[2:])
        pairsTags = zip(tags[:-1], tags[1:])
        tagSet = tagSet.union(tags)
        tripletCounter.update(tripletsTags)
        pairsCounter.update(pairsTags)
        onesCounter.update(tags)

    for tag1 in tagSet:
        for tag2 in tagSet:
            for tag3 in tagSet:
                qMle[(tag1, tag2, tag3)] = []
                qMle[(tag1, tag2, tag3)].append(
                    float(tripletCounter[(tag1, tag2, tag3)]) / max(pairsCounter[(tag1, tag2)], 1))
                qMle[(tag1, tag2, tag3)].append(float(pairsCounter[(tag2, tag3)]) / onesCounter[tag2])
                qMle[(tag1, tag2, tag3)].append(float(onesCounter[tag3]) / numWords)

    return qMle
