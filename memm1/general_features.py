from memm1.feature import Feature
from memm1.featurebuilder import FeatureBuilder


class LastTagAndCurrentTag(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "LastTagAndCurrentTag(last_tag=%s)" % self.history['ti-1']

    def __eq__(self, other):
        if isinstance(other, LastTagAndCurrentTag):
            return self.history['ti-1'] == other.history['ti-1']
        return False

    def test(self, current_history):
        return self.history['ti-1'] == current_history['ti-1']


class LastTagAndCurrentTagBuilder(FeatureBuilder):
    def __init__(self):
        pass

    def from_history(self, history):
        return LastTagAndCurrentTag(history)


class LastTwoTagsAndCurrentTag(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "LastTwoTagsAndCurrentTag(pre_last_tag=%s,last_tag=%s)" % (self.history['ti-2'], self.history['ti-1'])

    def __eq__(self, other):
        if isinstance(other, LastTwoTagsAndCurrentTag):
            return self.history['ti-2'] == other.history['ti-2'] and self.history['ti-1'] == other.history['ti-1']
        return False

    def test(self, current_history):
        return self.history['ti-2'] == current_history['ti-2'] and self.history['ti-1'] == current_history['ti-1']


class LastTwoTagsAndCurrentTagBuilder(FeatureBuilder):
    def __init__(self):
        pass

    def from_history(self, history):
        return LastTwoTagsAndCurrentTag(history)


class LastWordAndCurrentTag(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "LastWordAndCurrentTag(last_word=%s)" % self.history['wi-1']

    def __eq__(self, other):
        if isinstance(other, LastWordAndCurrentTag):
            return self.history['wi-1'] == other.history['wi-1']
        return False

    def test(self, current_history):
        return self.history['wi-1'] == current_history['wi-1']


class LastWordAndCurrentTagBuilder(FeatureBuilder):
    def __init__(self):
        pass

    def from_history(self, history):
        return LastWordAndCurrentTag(history)


class WordBeforeLastWordAndCurrentTag(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "WordBeforeLastWordAndCurrentTag(word_before_last_word=%s)" % self.history['wi-2']

    def __eq__(self, other):
        if isinstance(other, WordBeforeLastWordAndCurrentTag):
            return self.history['wi-2'] == other.history['wi-2']
        return False

    def test(self, current_history):
        return self.history['wi-2'] == current_history['wi-2']


class WordBeforeLastWordAndCurrentTagBuilder(FeatureBuilder):
    def __init__(self):
        pass

    def from_history(self, history):
        return WordBeforeLastWordAndCurrentTag(history)


class NextWordAndCurrentTag(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "NextWordAndCurrentTag(next_word=%s)" % self.history['wi+1']

    def __eq__(self, other):
        if isinstance(other, NextWordAndCurrentTag):
            return self.history['wi+1'] == other.history['wi+1']
        return False

    def test(self, current_history):
        return self.history['wi+1'] == current_history['wi+1']


class NextWordAndCurrentTagBuilder(FeatureBuilder):
    def __init__(self):
        pass

    def from_history(self, history):
        return NextWordAndCurrentTag(history)


class WordAfterNextWordAndCurrentTag(Feature):
    def __init__(self, history):
        self.history = history

    def __repr__(self):
        return "WordAfterNextWordAndCurrentTag(word_after_next_word=%s)" % self.history['wi+2']

    def __eq__(self, other):
        if isinstance(other, WordAfterNextWordAndCurrentTag):
            return self.history['wi+2'] == other.history['wi+2']
        return False

    def test(self, current_history):
        return self.history['wi+2'] == current_history['wi+2']


class WordAfterNextWordAndCurrentTagBuilder(FeatureBuilder):
    def __init__(self):
        pass

    def from_history(self, history):
        return WordAfterNextWordAndCurrentTag(history)


class GeneralFeatures():
    FEATURES = [LastTagAndCurrentTagBuilder(), LastTwoTagsAndCurrentTagBuilder(), LastWordAndCurrentTagBuilder(),
                WordBeforeLastWordAndCurrentTagBuilder(), NextWordAndCurrentTagBuilder(),
                WordAfterNextWordAndCurrentTagBuilder()]
