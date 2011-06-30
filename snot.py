"""Monkey-patch unittest to pop the tb info we care about.
"""
import os
import pprint
import re
import sys
import traceback
import unittest

from nose.plugins import Plugin
from nose.plugins.capture import Capture
from nose.util import ln
from unittest import TestResult


class Snot(Capture):
    """Snot is colored output from nose.
    """

    name = "snot"

    def help(self):
        return self.__doc__

    def options(self, parser, env):
        """Override to un-conflict options with parent plugin.
        """
        Plugin.options(self, parser, env)

    def addCaptureToErr(self, ev, output):
        """Override to highlight captured output.
        """
        return '\n'.join([ str(ev) 
                         , ln('>> begin captured stdout <<')
                         , '\033[1;36m' + output + '\033[0m'
                         , ln('>> end captured stdout <<')
                          ])

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
    nlines = len(msgLines)
    if nlines > 1:

        # Highlight the error message.
        msgLines[-1] = actual.highlight(msgLines[-1])

        # Highlight the file at the bottom of the stack.
        i = -2
        if msgLines[i].strip() == '^':
            # For a SyntaxError we get a line of code and a caret indicating a
            # position in that line. Back up two more line in that case.
            i = -4
        msgLines[i] = fileinfo.highlight(msgLines[i])

        # Highlight the file with the breaking test.
        for i in range(nlines):
            if 'test_' in msgLines[i]:
                msgLines[i] = fileinfo.highlight(msgLines[i])
                break
    #
    ############################### end new

    if hasattr(self, 'buffer'):
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
