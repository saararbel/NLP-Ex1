from collections import Counter


def calc_e_prob(words, tags, wordAndTags):
    eMle = {}
    tagsSet = set(tags)
    tagsCounter = Counter(tags)
    wordAndTagsCounter = Counter(wordAndTags)

    for word in set(words):
        for tag in tagsSet:
            eMle[(word, tag)] = float(wordAndTagsCounter[(word, tag)]) / tagsCounter[tag]

    return eMle


def calcQprob(tags, numWords):
    qMle = {}
    tripletsTags = zip(['start', 'start'] + tags[:-2], ['start'] + tags[:-1], tags)
    pairsTags = zip(['start'] + tags[:-1], tags)

    tagSet = set(tags)
    tripletCounter = Counter(tripletsTags)
    pairsCounter = Counter(pairsTags)
    onesCounter = Counter(tags)

    for tag1 in tagSet:
        for tag2 in tagSet:
            for tag3 in tagSet:
                if (tag1, tag2, tag3) not in qMle:
                    qMle[(tag1, tag2, tag3)] = []
                qMle[(tag1, tag2, tag3)].append(
                    float(tripletCounter[(tag1, tag2, tag3)]) / max(pairsCounter[(tag1, tag2)], 1))
                qMle[(tag1, tag2, tag3)].append(float(pairsCounter[(tag2, tag3)]) / onesCounter[tag2])
                qMle[(tag1, tag2, tag3)].append(float(onesCounter[tag3]) / numWords)

    return qMle
