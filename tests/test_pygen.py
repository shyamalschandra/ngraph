# ----------------------------------------------------------------------------
# Copyright 2017 Nervana Systems Inc.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ----------------------------------------------------------------------------

from ngraph.util.pygen import PyGen
import numpy as np


class HelloCodeGenerator(PyGen):

    def __init__(self, **kwargs):
        super(HelloCodeGenerator, self).__init__(prefix="gentest", **kwargs)

    def name(self, x):
        return x

    def generate_hello(self):
        self.append("""
def hello(who):
    return "Hello " + who + "!" """)
        self.endl()
        r = self.compile()
        return r['hello']

    def generate_try_twice(self):
        self.append("""
def try_twice(who):
    return hello(who) + "|" + hello(who)""")
        self.endl()
        return self.compile()['try_twice']

    def generate_make_list(self):
        self.append("""
def make_list():
    return list()""")
        self.endl()
        return self.compile()['make_list']


def test_hello():
    generator = HelloCodeGenerator()
    hello = generator.generate_hello()
    value = hello("World")
    assert value == "Hello World!"

    # Try to call previous function
    try_twice = generator.generate_try_twice()
    value = try_twice("World")
    assert value == "Hello World!|Hello World!"

    make_list = generator.generate_make_list()
    value = make_list()
    assert value == []

    # Try imports
    generator.execute("import numpy as np")
    value = generator.evaluate("np.zeros(5)")
    assert np.allclose(value, np.zeros(5))
