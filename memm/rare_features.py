import re

from memm.feature import Feature
from memm.featurebuilder import FeatureBuilder

RE_D = re.compile('\d')
RE_HYPHEN = re.compile('-')
RE_CAPITAL = re.compile('[A-Z]')


class PrefixAndSize(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "PrefixAndSize(word=%s,tag=%s)" % (self.history['wi'], self.history['ti'])

    def __eq__(self, other):
        if isinstance(other, PrefixAndSize):
            return self.history['wi'] == other.history['wi'] and self.history['ti'] == other.history['ti']
        return False

    def test(self, current_history):
        return self.history['ti'] == current_history['ti'] and len(current_history['wi']) <= 4 and \
               self.history['wi'].startswith(current_history['wi'])


class PrefixAndSizeBuilder(FeatureBuilder):
    def from_history(self, history):
        return PrefixAndSize(history)


class SuffixAndSize(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "SuffixAndSize(word=%s,tag=%s)" % (self.history['wi'], self.history['ti'])

    def __eq__(self, other):
        if isinstance(other, SuffixAndSize):
            return self.history['wi'] == other.history['wi'] and self.history['ti'] == other.history['ti']
        return False

    def test(self, current_history):
        return self.history['ti'] == current_history['ti'] and len(current_history['wi']) <= 4 and self.history[
            'wi'].endswith(current_history['wi'])


class SuffixAndSizeBuilder(FeatureBuilder):
    def from_history(self, history):
        return SuffixAndSize(history)


class ContainsANumber(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "ContainsANumber(tag=%s)" % (self.history['ti'])

    def __eq__(self, other):
        if isinstance(other, ContainsANumber):
            return self.history['ti'] == other.history['ti']
        return False

    def test(self, current_history):
        return bool(RE_D.search(current_history['wi']))
        # return any(char.isdigit() for char in current_history['wi']) and self.history['ti'] == current_history['ti']


class ContainsANumberBuilder(FeatureBuilder):
    def from_history(self, history):
        return ContainsANumber(history)


class ContainsAnUpperCase(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "ContainsAnUpperCase(tag=%s)" % (self.history['ti'])

    def __eq__(self, other):
        if isinstance(other, ContainsAnUpperCase):
            return self.history['ti'] == other.history['ti']
        return False

    def test(self, current_history):
        return bool(RE_CAPITAL.search(current_history['wi']))
        # return any(char.isupper() for char in current_history['wi']) and self.history['ti'] == current_history['ti']


class ContainsAnUpperCaseBuilder(FeatureBuilder):
    def from_history(self, history):
        return ContainsAnUpperCase(history)


class ContainsAnHyphen(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "ContainsAnHyphen(tag=%s)" % (self.history['ti'])

    def __eq__(self, other):
        if isinstance(other, ContainsAnHyphen):
            return self.history['ti'] == other.history['ti']
        return False

    def test(self, current_history):
        return bool(RE_HYPHEN.search(current_history['wi']))
        # return any(char == '-' for char in current_history['wi']) and self.history['ti'] == current_history['ti']


class ContainsAnHyphenBuilder(FeatureBuilder):
    def from_history(self, history):
        return ContainsAnHyphen(history)


class RareFeatures():
    FEATURES = [PrefixAndSizeBuilder(), SuffixAndSizeBuilder(), ContainsANumberBuilder(), ContainsAnUpperCaseBuilder(),
                ContainsAnHyphenBuilder()]
