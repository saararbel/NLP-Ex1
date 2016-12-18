from abc import ABCMeta, abstractmethod


class FeatureBuilder():
    __metaclass__ = ABCMeta

    @abstractmethod
    def from_history(self, history):
        pass
