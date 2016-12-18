from abc import ABCMeta, abstractmethod


class Feature():
    __metaclass__ = ABCMeta

    @abstractmethod
    def test(self, current_history):
        pass

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass
