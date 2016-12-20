import re

from memm1.feature import Feature
from memm1.featurebuilder import FeatureBuilder
from memm1.general_features import GeneralFeatures

RE_D = re.compile('\d')
RE_HYPHEN = re.compile('-')
RE_CAPITAL = re.compile('[A-Z]')


class Prefix(Feature):
    def __init__(self, prefix):
        self.prefix = prefix

    def __repr__(self):
        return "Prefix(prefix=%s)" % self.prefix

    def __eq__(self, other):
        if isinstance(other, Prefix):
            return self.prefix == other.prefix
        return False

    def test(self, current_history):
        return current_history.startswith(self.prefix)


def prefixed(word):
    return [word[:i] for i in xrange(1, min(5, len(word)))]


class PrefixBuilder(FeatureBuilder):
    def multiple_from_history(self, history):
        return [Prefix(history['wi'][:i]) for i in xrange(1, min(5, len(history['wi'])))]


class Suffix(Feature):
    def __init__(self, suffix):
        self.suffix = suffix

    def __repr__(self):
        return "Suffix(suffix=%s)" % self.suffix

    def __eq__(self, other):
        if isinstance(other, Suffix):
            return self.suffix == other.suffix
        return False

    def test(self, current_history):
        return current_history.endswith(self.suffix)


class SuffixBuilder(FeatureBuilder):
    def multiple_from_history(self, history):
        return [Suffix(history['wi'][-i:]) for i in xrange(1, min(5, len(history['wi'])))]


class ContainsANumber(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "ContainsANumber"

    def __eq__(self, other):
        return isinstance(other, ContainsANumber)

    def test(self, current_history):
        return bool(RE_D.search(current_history['wi']))


class ContainsANumberBuilder(FeatureBuilder):
    def from_history(self, history):
        return ContainsANumber(history)


class ContainsAnUpperCase(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "ContainsAnUpperCase"

    def __eq__(self, other):
        return isinstance(other, ContainsAnUpperCase)

    def test(self, current_history):
        return bool(RE_CAPITAL.search(current_history['wi']))


class ContainsAnUpperCaseBuilder(FeatureBuilder):
    def from_history(self, history):
        return ContainsAnUpperCase(history)


class ContainsAnHyphen(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "ContainsAnHyphen"

    def __eq__(self, other):
        return isinstance(other, ContainsAnHyphen)

    def test(self, current_history):
        return bool(RE_HYPHEN.search(current_history['wi']))


class ContainsAnHyphenBuilder(FeatureBuilder):
    def from_history(self, history):
        return ContainsAnHyphen(history)


class RareFeatures():
    ONLY_RARE = [PrefixBuilder(), SuffixBuilder(), ContainsANumberBuilder(), ContainsAnUpperCaseBuilder(),
                 ContainsAnHyphenBuilder()]
    FEATURES = GeneralFeatures.FEATURES + ONLY_RARE
