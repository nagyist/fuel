import numpy
from numpy.testing import assert_raises
from six.moves import cPickle

from fuel.datasets import MNIST
from tests import skip_if_not_available


def test_mnist():
    skip_if_not_available(datasets=['mnist'])
    mnist_train = MNIST('train', start=20000)
    assert len(mnist_train.features) == 40000
    assert len(mnist_train.targets) == 40000
    assert mnist_train.num_examples == 40000
    mnist_test = MNIST('test', sources=('targets',))
    assert len(mnist_test.targets) == 10000
    assert mnist_test.num_examples == 10000

    first_feature, first_target = mnist_train.get_data(request=[0])
    assert first_feature.shape == (1, 784)
    assert first_feature.dtype.kind == 'f'
    assert first_target.shape == (1, 1)
    assert first_target.dtype is numpy.dtype('uint8')

    first_target, = mnist_test.get_data(request=[0, 1])
    assert first_target.shape == (2, 1)

    binary_mnist = MNIST('test', binary=True, sources=('features',))
    first_feature, = binary_mnist.get_data(request=[0])
    assert first_feature.dtype.kind == 'b'
    assert_raises(ValueError, MNIST, 'valid')

    mnist_train = cPickle.loads(cPickle.dumps(mnist_train))
    assert len(mnist_train.features) == 40000

    mnist_test_unflattened = MNIST('test', flatten=False)
    assert mnist_test_unflattened.features.shape == (10000, 28, 28)
