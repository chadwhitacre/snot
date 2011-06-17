"""Monkey-patch unittest to pop the tb info we care about.
"""
import os
import pprint
import re
import sys
import traceback
import unittest

from nose.plugins import Plugin 
from unittest import TestResult


class Snot(Plugin):
    """Snot is colored output from nose.
    """
    # This is a stub to get nose to give us --with-snot.

    name = "snot"

    def help(self):
        return self.__doc__


class Highlighter:

    def __init__(self, pattern, highlight):
        self.__pattern = re.compile(pattern)
        self.__highlight = highlight

    def highlight(self, line):
        return self.__pattern.sub(self.__highlight, line)


fileinfo = Highlighter( r'^(.*"/?(?:.*/)*)([^"]+)", line (\d+)'
                      , r'\1\033[1;31m\2\033[0m", line \033[1;31m\3\033[0m'
                       )

def try_to_pretty_print(match):
    exc = match.group(1)
    msg = match.group(2)
    if exc == 'AssertionError':
        try:
            # If an AssertionError gives us a Python data structure, we want to
            # format that nicely.
            msg = eval(msg)
            msg = pprint.pformat(msg, width=75)
            if os.linesep in msg:
                msg = os.linesep.join(['    ' + x for x in msg.splitlines()])
                msg = os.linesep + os.linesep + msg
        except:
            pass
    msg = '\033[1;36m' + msg + '\033[0m'
    return '\033[1;31m' + exc + '\033[0m: ' + msg

actual = Highlighter(r'^([^:]+): (.*)$', try_to_pretty_print)


def _exc_info_to_string(self, err, test):
    """Converts a sys.exc_info()-style tuple of values into a string.
    
    Overriden to add ANSI color escapes at key moments. 

    """
    exctype, value, tb = err
    # Skip test runner traceback levels
    while tb and self._is_relevant_tb_level(tb):
        tb = tb.tb_next

    if exctype is test.failureException:
        # Skip assert*() traceback levels
        length = self._count_relevant_tb_levels(tb)
        msgLines = traceback.format_exception(exctype, value, tb, length)
    else:
        msgLines = traceback.format_exception(exctype, value, tb)

    ############################### begin new
    #
    if len(msgLines) > 1:
        msgLines[-2] = fileinfo.highlight(msgLines[-2])
        msgLines[-1] = actual.highlight(msgLines[-1])
    #
    ############################### end new

    if self.buffer:
        output = sys.stdout.getvalue()
        error = sys.stderr.getvalue()
        if output:
            if not output.endswith('\n'):
                output += '\n'
            msgLines.append(STDOUT_LINE % output)
        if error:
            if not error.endswith('\n'):
                error += '\n'
            msgLines.append(STDERR_LINE % error)
    return ''.join(msgLines)

TestResult._exc_info_to_string = _exc_info_to_string


class Tests(unittest.TestCase):

    def test_success(self):
        pass

    def test_failure(self):
        self.assertTrue(False) 

    def test_error(self):
        raise heck


if __name__ == '__main__':
    import unittest
    unittest.main()
