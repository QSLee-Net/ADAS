import tensorflow as tf

class KerasObject:
    _backend = tf.keras.backend
    _models = tf.keras.models
    _layers = tf.keras.layers
    _utils = tf.keras.utils

    def __init__(self, name=None):
        if (self.backend is None or
                self.utils is None or
                self.models is None or
                self.layers is None):
            raise RuntimeError('You cannot use `KerasObjects` with None submodules.')

        self._name = name

    @property
    def __name__(self):
        if self._name is None:
            return self.__class__.__name__
        return self._name

    @property
    def name(self):
        return self.__name__

    @name.setter
    def name(self, name):
        self._name = name

    @classmethod
    def set_submodules(cls, backend, layers, models, utils):
        cls._backend = backend
        cls._layers = layers
        cls._models = models
        cls._utils = utils

    @property
    def submodules(self):
        return {
            'backend': self.backend,
            'layers': self.layers,
            'models': self.models,
            'utils': self.utils,
        }

    @property
    def backend(self):
        return self._backend

    @property
    def layers(self):
        return self._layers

    @property
    def models(self):
        return self._models

    @property
    def utils(self):
        return self._utils


class Metric(KerasObject):
    pass


class Loss(KerasObject):

    def __add__(self, other):
        if isinstance(other, Loss):
            return SumOfLosses(self, other)
        else:
            raise ValueError('Loss should be inherited from `Loss` class')

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return MultipliedLoss(self, value)
        else:
            raise ValueError('Loss should be inherited from `BaseLoss` class')

    def __rmul__(self, other):
        return self.__mul__(other)


class MultipliedLoss(Loss):

    def __init__(self, loss, multiplier):

        # resolve name
        if len(loss.__name__.split('+')) > 1:
            name = '{}({})'.format(multiplier, loss.__name__)
        else:
            name = '{}{}'.format(multiplier, loss.__name__)
        super().__init__(name=name)
        self.loss = loss
        self.multiplier = multiplier

    def __call__(self, gt, pr):
        return self.multiplier * self.loss(gt, pr)


class SumOfLosses(Loss):

    def __init__(self, loss1, loss2):
        name = '{}_plus_{}'.format(loss1.__name__, loss2.__name__)
        super().__init__(name=name)
        self.loss1 = loss1
        self.loss2 = loss2

    def __call__(self, gt, pr):
        return self.loss1(gt, pr) + self.loss2(gt, pr)
