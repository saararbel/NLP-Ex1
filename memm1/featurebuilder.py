from abc import ABCMeta


class FeatureBuilder():
    __metaclass__ = ABCMeta

    def from_history(self, history):
        raise NotImplementedError

    def multiple_from_history(self, history):
        return [self.from_history(history)]
