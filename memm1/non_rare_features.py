from memm1.feature import Feature
from memm1.featurebuilder import FeatureBuilder
from memm1.general_features import GeneralFeatures


class WordAndTag(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "WordAndTag(word=%s)" % self.history['wi']

    def __eq__(self, other):
        if isinstance(other, WordAndTag):
            return self.history['wi'] == other.history['wi']
        return False

    def test(self, current_history):
        return self.history['wi'] == current_history['wi']


class WordAndTagBuilder(FeatureBuilder):
    def from_history(self, history):
        return WordAndTag(history)


class NotRareFeatures():
    FEATURES = GeneralFeatures.FEATURES + [WordAndTagBuilder()]
