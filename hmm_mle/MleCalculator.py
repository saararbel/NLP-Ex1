from collections import Counter


def calc_e_prob(words, tag_lines, wordAndTags):
    eMle = {}
    tagsSet = set()
    tagsCounter = Counter()
    for tags in tag_lines:
        tagsSet = tagsSet.union(tags)
        tagsCounter.update(tags)
    wordAndTagsCounter = Counter(wordAndTags)

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
