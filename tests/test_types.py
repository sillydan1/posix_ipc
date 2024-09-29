"""Test that the stubs generated by pybind11-stubgen are compatible with the hand-crafted ones."""

import inspect
import os
import sys
import unittest
from unittest.mock import patch

import posix_ipc as handcrafted
from pybind11_stubgen import main

from . import base as tests_base


class TestPybind11TypesCompatibility(tests_base.Base):
    """Test that the stubs generated by pybind11-stubgen are compatible with the hand-crafted ones."""

    def setUp(self):
        """Generate the type stubs."""
        # mock the sys.argv - I dont want to do a subprocess.run because it can be error prone depending on which
        # packages you may have installed.
        with patch.object(sys, 'argv', ["pybind11-stubgen", "posix_ipc", "-o", "tests/stubs"]):
            main()
        os.rename("tests/stubs/posix_ipc.pyi", "tests/stubs/__init__.py")  # to make the stubs importable

    def test_messagequeue(self):
        """Test the generated MessageQueue is the same as the hand-crafted one."""
        from . import stubs as generated
        generated_methods = inspect.getmembers(generated.MessageQueue, predicate=inspect.ismethod)
        crafted_methods = inspect.getmembers(handcrafted.MessageQueue, predicate=inspect.ismethod)
        crafted_method_names = [m[0] for m in crafted_methods]
        for method in generated_methods:
            self.assertTrue(method[0] in crafted_method_names)
            # NOTE: We can't compare the func signatures, because pybind11-stubgen doesnt generate types for parameters.


if __name__ == '__main__':
    unittest.main()
