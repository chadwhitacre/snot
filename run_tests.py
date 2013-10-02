#!/usr/bin/env python
"""This script demonstrates installing snot in a unittest-based runner.
"""
import unittest

import snot


snot.install(unittest)
unittest.main(module='tests')
