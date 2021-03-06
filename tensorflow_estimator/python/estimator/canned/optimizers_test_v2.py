# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Tests for optimizers.py."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.framework import test_util
from tensorflow.python.platform import test
from tensorflow.python.training import adagrad
from tensorflow.python.training import adam
from tensorflow.python.training import ftrl
from tensorflow.python.training import gradient_descent
from tensorflow.python.training import optimizer as optimizer_lib
from tensorflow.python.training import rmsprop
from tensorflow_estimator.python.estimator.canned import optimizers


class _TestOptimizerV2(optimizer_lib.Optimizer):

  def __init__(self):
    super(_TestOptimizerV2, self).__init__(
        use_locking=False, name='TestOptimizer')


@test_util.run_all_in_graph_and_eager_modes
class GetOptimizerInstanceV2(test.TestCase):

  def test_unsupported_name(self):
    with self.assertRaisesRegexp(
        ValueError, 'Unsupported optimizer name: unsupported_name'):
      optimizers.get_optimizer_instance_v2(
          'unsupported_name', learning_rate=0.1)

  def test_adagrad_but_no_learning_rate(self):
    opt = optimizers.get_optimizer_instance_v2('Adagrad')
    self.assertIsInstance(opt, adagrad.AdagradOptimizer)
    self.assertAlmostEqual(0.05, opt._learning_rate)

  def test_adam_but_no_learning_rate(self):
    opt = optimizers.get_optimizer_instance_v2('Adam')
    self.assertIsInstance(opt, adam.AdamOptimizer)
    self.assertAlmostEqual(0.001, opt._lr)

  def test_adagrad(self):
    opt = optimizers.get_optimizer_instance_v2('Adagrad', learning_rate=0.1)
    self.assertIsInstance(opt, adagrad.AdagradOptimizer)
    self.assertAlmostEqual(0.1, opt._learning_rate)

  def test_adam(self):
    opt = optimizers.get_optimizer_instance_v2('Adam', learning_rate=0.1)
    self.assertIsInstance(opt, adam.AdamOptimizer)
    self.assertAlmostEqual(0.1, opt._lr)

  def test_ftrl(self):
    opt = optimizers.get_optimizer_instance_v2('Ftrl', learning_rate=0.1)
    self.assertIsInstance(opt, ftrl.FtrlOptimizer)
    self.assertAlmostEqual(0.1, opt._learning_rate)

  def test_rmsprop(self):
    opt = optimizers.get_optimizer_instance_v2('RMSProp', learning_rate=0.1)
    self.assertIsInstance(opt, rmsprop.RMSPropOptimizer)
    self.assertAlmostEqual(0.1, opt._learning_rate)

  def test_sgd(self):
    opt = optimizers.get_optimizer_instance_v2('SGD', learning_rate=0.1)
    self.assertIsInstance(opt, gradient_descent.GradientDescentOptimizer)
    self.assertAlmostEqual(0.1, opt._learning_rate)

  def test_object(self):
    opt = optimizers.get_optimizer_instance_v2(_TestOptimizerV2())
    self.assertIsInstance(opt, _TestOptimizerV2)

  def test_object_invalid(self):
    with self.assertRaisesRegexp(
        ValueError, 'The given object is not an Optimizer instance'):
      optimizers.get_optimizer_instance_v2((1, 2, 3))

  def test_callable(self):

    def _optimizer_fn():
      return _TestOptimizerV2()

    opt = optimizers.get_optimizer_instance_v2(_optimizer_fn)
    self.assertIsInstance(opt, _TestOptimizerV2)

  def test_lambda(self):
    opt = optimizers.get_optimizer_instance_v2(lambda: _TestOptimizerV2())  # pylint: disable=unnecessary-lambda
    self.assertIsInstance(opt, _TestOptimizerV2)

  def test_callable_returns_invalid(self):

    def _optimizer_fn():
      return (1, 2, 3)

    with self.assertRaisesRegexp(
        ValueError, 'The given object is not an Optimizer instance'):
      optimizers.get_optimizer_instance_v2(_optimizer_fn)


if __name__ == '__main__':
  test.main()
