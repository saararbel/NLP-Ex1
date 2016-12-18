from memm.feature import Feature
from memm.featurebuilder import FeatureBuilder


class WordAndTag(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "WordAndTag(word=%s,tag=%s)" % (self.history['wi'], self.history['ti'])

    def __eq__(self, other):
        if isinstance(other, WordAndTag):
            return self.history['wi'] == other.history['wi'] and self.history['ti'] == other.history['ti']
        return False

    def test(self, current_history):
        return self.history['wi'] == current_history['wi'] and self.history['ti'] == current_history['ti']


class WordAndTagBuilder(FeatureBuilder):
    def from_history(self, history):
        return WordAndTag(history)


class NotRareFeatures():
    FEATURES = [WordAndTagBuilder()]
